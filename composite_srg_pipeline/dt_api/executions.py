from typing import Optional

from httpx import Client as HttpxClient

from composite_srg_pipeline.models.dt_automation import TaskExecutions as TaskExecutionsModel
from composite_srg_pipeline.models.dt_enums import TaskResult as TaskResultEnum

from .authentication import get_oauth_token


def get_task_status(tenant_id: str, execution_id: str, task_id: str) -> Optional[TaskResultEnum]:

    result = None

    with HttpxClient() as client:
        r = client.get(
            f"https://{tenant_id}.apps.dynatrace.com/platform/automation/v1/executions/{execution_id}/tasks",
            headers={
                "Authorization": f"Bearer {get_oauth_token(scope=['automation:workflows:read']).access_token.get_secret_value()}"
            },
        )
        r.raise_for_status()

    tasks = TaskExecutionsModel(**r.json()).root

    for k, v in tasks.items():
        if k == task_id:
            result = TaskResultEnum(v.result.get("validation_status"))

    return result
