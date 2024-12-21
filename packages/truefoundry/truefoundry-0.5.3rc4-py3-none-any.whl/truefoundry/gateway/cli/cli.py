import click

from truefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from truefoundry.cli.display_util import print_entity_list
from truefoundry.gateway.lib.models import generate_code_for_model, list_models


def get_gateway_cli():
    @click.group(cls=GROUP_CLS, help="Commands to interact with TrueFoundry Gateway")
    def gateway(): ...

    @gateway.group("list", cls=GROUP_CLS, help="List gateway resources")
    def list_group():
        """List gateway resources"""
        pass

    @list_group.command(
        "models", cls=COMMAND_CLS, help="List available models filtered by type"
    )
    @click.option(
        "--type",
        "model_type",
        type=click.Choice(["chat", "completion", "embedding"]),
        help="Filter models by type",
    )
    def list_models_cli(model_type: str):
        enabled_models = list_models(model_type)
        print_entity_list("Models", enabled_models)

    @gateway.command("generate-code", cls=COMMAND_CLS, help="Generate code for a model")
    @click.argument("model_id")
    @click.option(
        "--inference-type",
        type=click.Choice(["chat", "completion", "embedding"]),
        default="chat",
        help="Type of inference to generate code for",
    )
    @click.option(
        "--client",
        type=click.Choice(["openai", "rest", "langchain", "stream", "node", "curl"]),
        default="curl",
        help="Language/framework to generate code for",
    )
    def generate_code_cli(model_id: str, inference_type: str, client: str):
        """Generate code for a model"""
        code = generate_code_for_model(
            model_id, client=client, inference_type=inference_type
        )
        print(code)

    return gateway
