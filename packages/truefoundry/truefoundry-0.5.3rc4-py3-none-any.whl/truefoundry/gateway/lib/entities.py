from typing import Any, Dict, List, Optional, Union

from truefoundry.pydantic_v1 import BaseModel


class GatewayModel(BaseModel):
    id: str
    name: str
    provider: str
    model_id: Optional[str]
    provider_account_name: str
    tfy_application_id: Optional[str] = None
    enabled: bool = True
    types: Union[str, List[str]] = ""
    created_by: str
    tenant_name: str
    model_fqn: str

    def list_row_data(self) -> Dict[str, Any]:
        model_display = self.model_fqn
        provider_display = self.provider
        if self.model_id:
            provider_display = f"{self.provider} ({self.model_id})"
        
        return {
            "model": model_display,
            "provider": provider_display,
            "type": self.types if isinstance(self.types, str) else ", ".join(self.types)
        }


class ProviderModels(BaseModel):
    __root__: Dict[str, Dict[str, List[GatewayModel]]]
