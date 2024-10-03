from composite_srg_pipeline.config import config, logger
from composite_srg_pipeline.dt_api import (
    check_workflow_completed_execution,
    get_task_status,
    get_workflow_execution_status,
    get_workflow_status,
    start_workflow,
)
from composite_srg_pipeline.models.dt_automation import ExecutionState as ExecutionStateEnum
from composite_srg_pipeline.models.dt_enums import TaskResult as TaskResultEnum


def composite_srg_execution_and_validation():
    srg_workflow_status = get_workflow_execution_status(
        tenant_id=config.tenant_id, workflow_id=str(config.srg_workflow_uuid)
    )

    if srg_workflow_status == ExecutionStateEnum.RUNNING:
        Exception(
            "There's a current execution of the Composite SRG workflow running.  Will not kick off another execution"
        )

    logger.info("Starting Composite SRG Workflow.")
    result = start_workflow(tenant_id=config.tenant_id, workflow_id=str(config.srg_workflow_uuid))
    if result.state != ExecutionStateEnum.RUNNING:
        raise Exception(f"Unexpected state '{result.state.value}' while attempting to start SRG Workflow.")

    logger.info("Composite SRG Workflow Started Successfully.")
    check_workflow_completed_execution(tenant_id=config.tenant_id, workflow_id=str(config.srg_workflow_uuid))

    logger.info("Checking result of Composite SRG.")
    workflow_status = get_workflow_status(tenant_id=config.tenant_id, workflow_id=str(config.srg_workflow_uuid))
    task_status = get_task_status(
        tenant_id=config.tenant_id,
        execution_id=str(workflow_status.lastExecution.id),
        task_id=config.srg_workflow_task_name,
    )
    if task_status != TaskResultEnum.success:
        raise Exception(f"An error was encountered with the SRGs. Retrieved status: {task_status.value}")
    logger.info("All SRGs passed their objectives successfully")


if __name__ == "__main__":
    composite_srg_execution_and_validation()
