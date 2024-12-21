from typing import List, Literal, Optional

from truefoundry.deploy.lib.clients.servicefoundry_client import (
    ServiceFoundryServiceClient,
)
from truefoundry.gateway.lib.client import GatewayServiceClient
from truefoundry.gateway.lib.entities import GatewayModel


def list_models(
    model_type: Optional[Literal["chat", "completion", "embedding"]] = None,
) -> List[GatewayModel]:
    """List available models filtered by type

    Args:
        model_type (Optional[str], optional): Filter models by type ('chat' or 'completion'). Defaults to None.

    Returns:
        List: List of enabled models
    """
    client = ServiceFoundryServiceClient()
    models = client.get_gateway_models(model_type)

    enabled_models = []
    for _, accounts in models.__root__.items():
        for _, model_list in accounts.items():
            for model in model_list:
                enabled_models.append(model)

    return enabled_models


def generate_code_for_model(
    model_id: str,
    client: Literal["openai", "rest", "langchain", "stream", "node", "curl"] = "curl",
    inference_type: Literal["chat", "completion", "embedding"] = "chat",
) -> str:
    """Generate code snippet for using a model in the specified language/framework

    Args:
        model_id (str): ID of the model to generate code for
        language (Literal["openai", "rest", "langchain", "stream", "node", "curl"]): Language/framework to generate code for. Defaults to "curl"
        inference_type (Literal["chat", "completion", "embedding"]): Type of inference to generate code for. Defaults to "chat"

    Returns:
        str: Code snippet for using the model in the specified language/framework
    """
    gateway_client = GatewayServiceClient()
    response = gateway_client.generate_code(model_id, inference_type)

    code_map = {
        "openai": ("openai_code", "Python code using OpenAI SDK for direct API calls"),
        "rest": ("rest_code", "Python code using requests library for REST API calls"),
        "langchain": (
            "langchain_code",
            "Python code using LangChain framework for LLM integration",
        ),
        "stream": ("stream_code", "Python code with streaming response handling"),
        "node": ("node_code", "Node.js code using Axios for API calls"),
        "curl": ("curl_code", "cURL command for direct API access via terminal"),
    }

    code_key, description = code_map[client]
    if code_key in response and response[code_key]:
        return f"{description}\n{response[code_key]}"

    return "No code snippet available for the specified language"
