"""This module defines the settings for everything related to the CLI."""

from typing import Optional
from urllib.parse import urlparse

from fideslang.validation import AnyHttpUrlString
from fideslog.sdk.python.utils import FIDESCTL_CLI, generate_client_id
from pydantic import Field, SerializeAsAny, ValidationInfo, field_validator
from pydantic_settings import SettingsConfigDict

from .fides_settings import FidesSettings, port_integer_converter

# pylint: disable=C0115,C0116, E0213

ENV_PREFIX = "FIDES__CLI__"


class CLISettings(FidesSettings):
    """Configuration settings for the command-line application."""

    analytics_id: str = Field(
        default=generate_client_id(FIDESCTL_CLI),
        description="A fully anonymized unique identifier that is automatically generated by the application. Used for anonymous analytics when opted-in.",
        validate_default=True,
    )
    local_mode: bool = Field(
        default=False,
        description="When set to True, disables functionality that requires making calls to a Fides webserver.",
    )
    server_protocol: str = Field(
        default="http", description="The protocol used by the Fides webserver."
    )
    server_host: str = Field(
        default="localhost", description="The hostname of the Fides webserver."
    )
    server_port: str = Field(
        default="8080", description="The port of the Fides webserver"
    )
    server_path: str = Field(default="/", description="The path of the Fides webserver")
    server_url: SerializeAsAny[Optional[AnyHttpUrlString]] = Field(
        default=None,
        description="The full server url generated from the other server configuration values.",
        exclude=True,
        validate_default=True,
    )

    @field_validator("server_url")
    @classmethod
    def get_server_url(cls, value: str, info: ValidationInfo) -> str:
        """Create the server_url from the server configuration values. Strips path if present."""
        host = info.data.get("server_host")
        protocol = info.data.get("server_protocol")
        port: int = port_integer_converter(info, "server_port")
        port_str: str = f":{port}" if port else ""
        server_url = f"{protocol}://{host}{port_str}"
        # check if the host var had a path included
        parsed = urlparse(server_url)
        if parsed.path:
            print(
                f"Warning: The server_host value '{host}' includes a path. This will be stripped. Please update the server_host value to '{parsed.netloc}'."
            )
            server_url = f"{parsed.scheme}://{parsed.netloc}{port_str}"
            print(f"The server_url: `{server_url}` will be used.")

        return server_url

    @field_validator("analytics_id")
    def ensure_not_empty(cls, value: str) -> str:
        """
        Validate that the `analytics_id` is not `""`.
        """
        return value if value != "" else generate_client_id(FIDESCTL_CLI)

    model_config = SettingsConfigDict(env_prefix=ENV_PREFIX, coerce_numbers_to_str=True)
