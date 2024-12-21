from typing import Literal, Optional

import requests

from truefoundry.common.constants import GATEWAY_SERVER_RELATIVE_PATH
from truefoundry.common.credential_provider import (
    CredentialProvider,
    EnvCredentialProvider,
    FileCredentialProvider,
)


class GatewayServiceClient:
    def __init__(
        self,
        credential_provider: Optional[CredentialProvider] = None,
        host: Optional[str] = None,
    ) -> None:
        if credential_provider is None:
            if EnvCredentialProvider.can_provide():
                credential_provider = EnvCredentialProvider()
            elif FileCredentialProvider.can_provide():
                credential_provider = FileCredentialProvider()
            else:
                raise Exception(
                    "No credentials found. Please login using `tfy login` or set TFY_API_KEY environment variable"
                )

        self._credential_provider = credential_provider
        self._host = credential_provider.base_url

    def _get_header(self):
        return {
            "Authorization": f"Bearer {self._credential_provider.token.access_token}"
        }

    @property
    def _base_url(self) -> str:
        return f"{self._host}/{GATEWAY_SERVER_RELATIVE_PATH}"

    def generate_code(
        self, model_id: str, inference_type: Literal["chat", "completion", "embedding"]
    ) -> str:
        url = f"{self._base_url}/api/inference/openai/generate-code-snippet"
        data = {
            "model": model_id,
            "playground_endpoint": self._base_url,
            "inference_type": inference_type,
        }
        response = requests.post(url, headers=self._get_header(), json=data)
        return response.json()
