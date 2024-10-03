from typing import List

from authlib.integrations.httpx_client import OAuth2Client

from composite_srg_pipeline.config import config
from composite_srg_pipeline.models.oauth_access_token import AccessToken as AccessTokenModel


def get_oauth_token(scope: List[str] = None) -> AccessTokenModel:
    if not scope:
        scope = []

    with OAuth2Client(config.client_id, config.client_secret.get_secret_value(), scope=" ".join(scope)) as client:
        token = client.fetch_token(str(config.token_url), grant_type="client_credentials")
    return AccessTokenModel(**token)
