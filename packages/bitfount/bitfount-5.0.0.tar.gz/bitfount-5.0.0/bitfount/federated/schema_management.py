"""Schema management utilities for the Pod."""

from __future__ import annotations

from dataclasses import asdict
import importlib
import logging
from typing import TYPE_CHECKING, Mapping, Optional, cast
from uuid import UUID

from prefect import (
    Task,
    get_client,
    get_run_logger,
    resume_flow_run,
    suspend_flow_run,
    task,
)
from prefect.cache_policies import NONE as NONE_CACHE_POLICY
from prefect.client.schemas.filters import (
    FlowFilter,
    FlowFilterId,
    FlowFilterName,
    FlowRunFilter,
    FlowRunFilterState,
    FlowRunFilterStateName,
)
from prefect.context import TaskRun
from prefect.states import State
from requests import HTTPError, RequestException

from bitfount import config
from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSourceInferrable,
)
from bitfount.data.datasources.utils import FileSystemFilter
from bitfount.data.persistence.base import DataPersister
from bitfount.data.persistence.sqlite import SQLiteDataPersister
from bitfount.data.schema import BitfountSchema, SchemaGenerationFromYieldData
from bitfount.federated.exceptions import PodRegistrationError
from bitfount.federated.types import DatasourceContainer, MinimalDatasourceConfig
from bitfount.hub.api import BitfountHub
from bitfount.hub.exceptions import SchemaUploadError
from bitfount.hub.helper import _create_bitfounthub
from bitfount.utils import _handle_fatal_error

if TYPE_CHECKING:
    from bitfount.federated.types import (
        HubConfig,
        MinimalSchemaGenerationConfig,
        MinimalSchemaUploadConfig,
    )

logger = logging.getLogger(__name__)


def _get_minimal_datasource_config(
    datasource_container: DatasourceContainer,
) -> MinimalDatasourceConfig:
    """Get minimal datasource configuration from a datasource container."""
    return MinimalDatasourceConfig(
        datasource_cls_name=type(datasource_container.datasource).__name__,
        name=datasource_container.name,
        datasource_args=datasource_container.data_config.datasource_args,
        file_system_filters=datasource_container.data_config.file_system_filters,
    )


def _setup_direct_datasource(datasource_config: MinimalDatasourceConfig) -> BaseSource:
    """Creates a BaseSource instance from a class and arguments."""
    # Get the class from the name
    try:
        datasource_cls: type[BaseSource] = getattr(
            importlib.import_module("bitfount.data"),
            datasource_config.datasource_cls_name,
        )
    except AttributeError as e:
        raise ImportError(
            f"Unable to import {datasource_config.datasource_cls_name} from bitfount."
        ) from e

    # Create datasource instance
    # For non-FileSystemIterableSourceInferrable classes, we construct as normal...
    if not issubclass(datasource_cls, FileSystemIterableSourceInferrable):
        datasource = datasource_cls(**datasource_config.datasource_args)
    # For FileSystemIterableSourceInferrable (and all subclasses), we additionally
    # ensure that data caching support is available
    else:
        data_persister: Optional[DataPersister]
        if "data_cache" in datasource_config.datasource_args:
            data_persister = datasource_config.datasource_args["data_cache"]
            logger.warning(
                f"Found existing data cache in datasource_args, will not override."
                f" data_cache={data_persister}"
            )
        elif config.settings.enable_data_cache:
            config.settings.paths.dataset_cache_dir.mkdir(parents=True, exist_ok=True)
            data_persister_path = (
                config.settings.paths.dataset_cache_dir
                / f"{datasource_config.name}_cache.sqlite"
            ).resolve()

            logger.info(
                f'Creating/retrieving cache for dataset "{datasource_config.name}"'
                f" at {data_persister_path}"
            )
            data_persister = SQLiteDataPersister(data_persister_path)
        else:
            logger.info(
                f"Data caching has been disabled; {config.settings.enable_data_cache}"
            )
            data_persister = None

        if datasource_config.file_system_filters is not None:
            logger.info("Applying file system filters to datasource")
            filter = FileSystemFilter(**asdict(datasource_config.file_system_filters))
            datasource_config.datasource_args.update({"filter": filter})

        datasource = datasource_cls(
            data_cache=data_persister, **datasource_config.datasource_args
        )

    # Check that the instance has correctly instantiated BaseSource
    if not datasource.is_initialised:
        raise ValueError(
            f"The configured datasource {datasource_config.datasource_cls_name}"
            f" does not extend BaseSource"
        )

    return datasource


def _register_dataset(
    hub_upload_config: MinimalSchemaUploadConfig, hub: BitfountHub
) -> None:
    """Register dataset with Bitfount Hub.

    If dataset is already registered, will update dataset details if anything has
    changed.

    Args:
        hub_upload_config: Configuration for uploading schema to hub.
        hub: Bitfount Hub to register the pod with.

    Raises:
        PodRegistrationError: if registration fails for any reason
    """
    try:
        logger.info("Registering/Updating details on Bitfount Hub.")
        hub.register_pod(
            hub_upload_config.public_metadata,
            hub_upload_config.pod_public_key,
            hub_upload_config.access_manager_public_key,
        )
    except (HTTPError, SchemaUploadError) as ex:
        logger.critical(f"Failed to register with hub: {ex}")
        raise PodRegistrationError("Failed to register with hub") from ex
    except RequestException as ex:
        logger.critical(f"Could not connect to hub: {ex}")
        raise PodRegistrationError("Could not connect to hub") from ex


class SchemaGenerationHooks:
    """Prefect hooks for schema generation."""

    @staticmethod
    def on_schema_worker_completion(tsk: Task, run: TaskRun, state: State) -> None:
        """Log completion of schema worker task."""
        logger = get_run_logger()
        logger.info(f"Task {tsk.name} completed")

    @staticmethod
    def on_schema_worker_failure(tsk: Task, run: TaskRun, state: State) -> None:
        """Log failure of schema worker task."""
        logger = get_run_logger()
        logger.error(f"Task {tsk.name} failed")


class SchemaManagement:
    """Schema management utilities for the Pod."""

    @staticmethod
    def is_prefect_server_healthy() -> bool:
        """Check if the Prefect server is up and running."""
        try:
            with get_client(sync_client=True) as client:
                response = client.api_healthcheck()
                if isinstance(response, Exception):
                    raise response
        except Exception:
            return False

        return True

    @staticmethod
    async def _get_active_flow_run(flow_name: str) -> UUID:
        """Get the ID of the most recent active run of a flow.

        Args:
            flow_name: Name of the flow to get the active run for.

        Returns:
            UUID: ID of the most recent active run of the flow.

        Raises:
            ValueError: If no active runs are found for the flow.
        """
        try:
            async with get_client() as client:
                # Search for the flow by name
                flows = await client.read_flows(
                    flow_filter=FlowFilter(name=FlowFilterName(any_=[flow_name]))
                )

                # If no flows found, return a message
                if not flows:
                    raise ValueError(f"Flow with name '{flow_name}' not found.")

                flow = flows[0]  # Assuming there is only one flow with that name

                # Get the flow runs for that flow, filtered by flow_id and running state
                flow_runs = await client.read_flow_runs(
                    flow_filter=FlowFilter(id=FlowFilterId(any_=[flow.id])),
                    flow_run_filter=FlowRunFilter(
                        state=FlowRunFilterState(
                            name=FlowRunFilterStateName(any_=["RUNNING"])
                        )
                    ),
                )

                if not flow_runs:
                    raise ValueError(f"No active runs found for flow '{flow_name}'.")

                # Assuming the most recent running flow is the one you want
                return cast(UUID, flow_runs[0].id)

        except Exception as e:
            logger.error(e)
            raise ValueError(f"Failed to get active run for flow '{flow_name}'.") from e

    @classmethod
    async def suspend_active_flow(cls, flow_name: str) -> Optional[UUID]:
        """Suspend the most recent active run of a flow.

        Args:
            flow_name: Name of the flow to suspend.

        Returns:
            ID of the suspended flow run if successful, otherwise None.
        """
        try:
            flow_run_id = await cls._get_active_flow_run(flow_name)
            await suspend_flow_run(flow_run_id=flow_run_id, timeout=None)
        except ValueError as e:
            logger.error(f"Failed to suspend flow '{flow_name}': {e}")
            return None

        return flow_run_id

    @classmethod
    async def resume_suspended_flow(
        cls,
        flow_run_id: Optional[UUID],
        datasource_containers: list[DatasourceContainer],
    ) -> None:
        """Resume a suspended flow run with updated datasource configs.

        Args:
            flow_run_id: ID of the flow run to resume.
            datasource_containers: List of all datasource containers which will be
                filtered to those with schema types that are not "full".
        """
        if flow_run_id is not None:
            logger.info("Resuming schema generation flow.")
            await resume_flow_run(
                flow_run_id,
                {
                    "datasource_configs": [
                        _get_minimal_datasource_config(ds)
                        for ds in datasource_containers
                        if ds.schema.schema_type is not None
                        and ds.schema.schema_type != "full"
                    ]
                },
            )

    @staticmethod
    @task(
        name="schema-worker",
        retries=3,
        retry_delay_seconds=5,
        on_completion=[SchemaGenerationHooks.on_schema_worker_completion],
        on_failure=[SchemaGenerationHooks.on_schema_worker_failure],
        cache_policy=NONE_CACHE_POLICY,
    )
    async def schema_worker(
        datasource_config: MinimalDatasourceConfig,
        schema_generation_config: MinimalSchemaGenerationConfig,
        schema_upload_config: MinimalSchemaUploadConfig,
        hub_config: HubConfig,
    ) -> tuple[str, str]:
        """Process each record in the dataset with the ability to cancel.

        Args:
            datasource_config: The datasource config to generate schema for.
            schema_generation_config: The schema generation config.
            schema_upload_config: The schema upload config.
            hub_config: The hub config.

        Returns:
            The datasource name and the schema as a JSON string.
        """
        # Get logger
        _logger = get_run_logger()
        _logger.info("Task started")

        # Create hub instance
        hub = _create_bitfounthub(
            username=hub_config.username, secrets=hub_config.secrets
        )

        # Create datasource from config
        datasource = _setup_direct_datasource(datasource_config)

        # Create schema
        schema = BitfountSchema(
            name=schema_generation_config.datasource_name,
            description=schema_generation_config.description,
            column_descriptions=cast(
                Optional[Mapping[str, str]],
                schema_generation_config.column_descriptions,
            ),
        )

        # Add hook to generate schema from data
        hook = SchemaGenerationFromYieldData(
            schema,
            schema_generation_config.ignore_cols,
            schema_generation_config.force_stypes,
        )
        datasource.add_hook(hook)

        # Process each record in the dataset
        for i, _ in enumerate(datasource.yield_data()):
            _logger.info(f"Processing batch {i}")
            # Iterate through all the data to populate the schema.
            try:
                schema_upload_config.public_metadata.schema = schema.to_json()
                _register_dataset(schema_upload_config, hub)
            except PodRegistrationError as pre:
                _handle_fatal_error(pre, logger=logger)

        schema.schema_type = "full"
        _logger.info("Schema generation task completed")

        try:
            schema_upload_config.public_metadata.schema = schema.to_json()
            _register_dataset(schema_upload_config, hub)
        except PodRegistrationError as pre:
            _handle_fatal_error(pre, logger=logger)

        return schema_generation_config.datasource_name, schema.dumps()
