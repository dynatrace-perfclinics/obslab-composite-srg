from httpx import Client as HttpxClient
from retry import retry

from composite_srg_pipeline.config import config, logger
from composite_srg_pipeline.exceptions import *
from composite_srg_pipeline.models.dt_automation import Execution as ExecutionModel
from composite_srg_pipeline.models.dt_automation import ExecutionState as ExecutionStateEnum
from composite_srg_pipeline.models.dt_automation import Workflow as WorkflowModel

from .authentication import get_oauth_token


def get_workflow_status(tenant_id: str, workflow_id: str) -> WorkflowModel:
    with HttpxClient() as client:
        r = client.get(
            f"https://{tenant_id}.apps.dynatrace.com/platform/automation/v1/workflows/{workflow_id}",
            headers={
                "Authorization": f"Bearer {get_oauth_token(scope=['automation:workflows:read', 'automation:workflows:run']).access_token.get_secret_value()}"
            },
        )
        r.raise_for_status()

    return WorkflowModel(**r.json())


def get_workflow_execution_status(tenant_id: str, workflow_id: str) -> ExecutionStateEnum:
    with HttpxClient() as client:
        r = client.get(
            f"https://{tenant_id}.apps.dynatrace.com/platform/automation/v1/workflows/{workflow_id}",
            headers={
                "Authorization": f"Bearer {get_oauth_token(scope=['automation:workflows:read', 'automation:workflows:run']).access_token.get_secret_value()}"
            },
        )
        r.raise_for_status()

    return WorkflowModel(**r.json()).lastExecution.state


def start_workflow(tenant_id: str, workflow_id: str) -> ExecutionModel:
    with HttpxClient() as client:
        r = client.post(
            f"https://{tenant_id}.apps.dynatrace.com/platform/automation/v1/workflows/{workflow_id}/run",
            headers={
                "Authorization": f"Bearer {get_oauth_token(scope=['automation:workflows:run']).access_token.get_secret_value()}"
            },
        )
        r.raise_for_status()

    return ExecutionModel(**r.json())


@retry(
    exceptions=WorkflowStillRunning,
    tries=config.workflow_retry_count,
    delay=config.workflow_retry_delay,
    max_delay=config.workflow_retry_max_delay,
)
def check_workflow_completed_execution(tenant_id: str, workflow_id: str) -> ExecutionStateEnum:
    logger.info("Retrieving Status of Workflow")

    workflow_execution_status = get_workflow_execution_status(tenant_id=tenant_id, workflow_id=workflow_id)
    logger.info(f"Workflow ID: {workflow_id} - Workflow Status: {workflow_execution_status.value}")

    if workflow_execution_status == ExecutionStateEnum.RUNNING:
        logger.info(
            f"Workflows & SRGs are still running.  Will sleep {config.workflow_retry_delay} seconds and check on status again."
        )
        raise WorkflowStillRunning("Workflow is still running")
    elif workflow_execution_status == ExecutionStateEnum.SUCCESS:
        return workflow_execution_status
    else:
        raise Exception("Workflow did not complete as expected")
