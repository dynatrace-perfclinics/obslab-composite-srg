from pydantic import BaseModel, Field, SecretStr


class AccessToken(BaseModel):
    scope: str = Field(title="scope", description="List of token scopes delineated by spaces")
    token_type: str = Field(title="Token Type")
    expires_in: int
    access_token: SecretStr = Field(title="Access Token", description="The end token used in subsequent requests")
    resource: str
    expires_at: int = Field(title="Expires At", description="Unix timestamp for when the token expires")
