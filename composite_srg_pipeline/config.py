# Unused import is actually imported in other files
# Defining the import here in the event we need to modify the logger
from loguru import logger
from pydantic import UUID4, AnyHttpUrl, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    token_url: AnyHttpUrl = Field(
        title="SSO system URL", description="The OAUTH2 URL used to request a bearer token", alias="DT_TOKEN_URL"
    )
    client_id: str = Field(title="OAUTH2 Client ID", alias="DT_CLIENT_ID")
    client_secret: SecretStr = Field(title="OAUTH2 Client Secret", alias="DT_CLIENT_SECRET")
    srg_workflow_uuid: UUID4 = Field(
        title="Composite SRG Workflow UUID",
        description="Dynatrace has a workflow used to orchestrate execution of all prerequisite SRGs. This should be set to the UUID of that workflow.",
        alias="DT_SRG_WORKFLOW_UUID",
    )
    srg_workflow_task_name: str = Field(
        title="Task Name for Composite SRG Execution",
        description="In the above Composite SRG Workflow, there is a single step which is responsible for executing the Composite SRG. This field should correpsond to that name.",
        alias="DT_TASK_NAME",
    )
    tenant_id: str = Field(
        title="Dynatrace Tenant UUID",
        description="The 8 character Tenant ID taken from https://<TENANT_ID>.apps.dynatrace.com/ui",
        alias="DT_TENANT_ID",
    )

    workflow_retry_count: int = Field(
        3,
        title="Workflow Retry Count",
        description="The number of attempts we will make to request the status of the Composite SRG Workflow before considering the execution a failure.",
        alias="WORKFLOW_RETRY_COUNT",
    )
    workflow_retry_delay: int = Field(
        50,
        title="Workflow Retry Delay",
        description="The time delay between retried API queries for Workflow status",
        alias="WORKFLOW_RETRY_DELAY",
    )
    workflow_retry_max_delay: int = Field(
        150,
        title="Workflow Retry Max Delay",
        description="The longest period of time we will await for a non 'RUNNING' Workflow Status result",
        alias="WORKFLOW_RETRY_MAX_DELAY",
    )

    @field_validator("token_url", mode="before")
    @classmethod
    def strip_trailing_slash(cls, v: str) -> str:
        return v.strip("/")


config = Config()
