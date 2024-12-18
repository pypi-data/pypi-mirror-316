"""
Type annotations for botocore.session module.

Copyright 2024 Vlad Emelianov
"""

from collections.abc import MutableMapping
from logging import Logger
from typing import IO, Any, Iterator, Mapping, Protocol

from botocore.client import BaseClient, Config
from botocore.compat import HAS_CRT as HAS_CRT
from botocore.configprovider import (
    BOTOCORE_DEFAUT_SESSION_VARIABLES as BOTOCORE_DEFAUT_SESSION_VARIABLES,
)
from botocore.configprovider import ConfigChainFactory as ConfigChainFactory
from botocore.configprovider import ConfigValueStore as ConfigValueStore
from botocore.configprovider import (
    create_botocore_default_config_mapping as create_botocore_default_config_mapping,
)
from botocore.credentials import Credentials
from botocore.errorfactory import ClientExceptionsFactory as ClientExceptionsFactory
from botocore.exceptions import ConfigNotFound as ConfigNotFound
from botocore.exceptions import PartialCredentialsError as PartialCredentialsError
from botocore.exceptions import ProfileNotFound as ProfileNotFound
from botocore.exceptions import UnknownServiceError as UnknownServiceError
from botocore.hooks import BaseEventHooks
from botocore.hooks import EventAliaser as EventAliaser
from botocore.hooks import HierarchicalEmitter as HierarchicalEmitter
from botocore.hooks import first_non_none_response as first_non_none_response
from botocore.loaders import create_loader as create_loader
from botocore.model import ServiceModel as ServiceModel
from botocore.paginate import PaginatorModel
from botocore.parsers import ResponseParserFactory as ResponseParserFactory
from botocore.regions import EndpointResolver as EndpointResolver
from botocore.tokens import FrozenAuthToken
from botocore.utils import EVENT_ALIASES as EVENT_ALIASES
from botocore.utils import validate_region_name as validate_region_name
from botocore.waiter import WaiterModel

logger: Logger = ...

class _EventHandler(Protocol):
    def __call__(self, **kwargs: Any) -> None: ...

class Session:
    SESSION_VARIABLES: dict[str, tuple[Any, Any, Any, Any]]
    LOG_FORMAT: str
    user_agent_name: str
    user_agent_version: str
    user_agent_extra: str
    session_var_map: SessionVarDict
    def __init__(
        self,
        session_vars: dict[str, tuple[Any, Any, Any, Any]] | None = ...,
        event_hooks: BaseEventHooks | None = ...,
        include_builtin_handlers: bool = ...,
        profile: str | None = ...,
    ) -> None: ...
    @property
    def available_profiles(self) -> list[str]: ...
    @property
    def profile(self) -> str | None: ...
    def get_config_variable(self, logical_name: str, methods: Any | None = ...) -> Any: ...
    def set_config_variable(self, logical_name: str, value: Any) -> None: ...
    def instance_variables(self) -> dict[str, Any]: ...
    def get_scoped_config(self) -> dict[str, Any]: ...
    @property
    def full_config(self) -> dict[str, Any]: ...
    def get_default_client_config(self) -> Config: ...
    def set_default_client_config(self, client_config: Config) -> None: ...
    def set_credentials(
        self, access_key: str, secret_key: str, token: str | None = ...
    ) -> None: ...
    def get_credentials(self) -> Credentials: ...
    def get_auth_token(self) -> FrozenAuthToken: ...
    def user_agent(self) -> str: ...
    def get_data(self, data_path: str) -> Any: ...
    def get_service_model(
        self, service_name: str, api_version: str | None = ...
    ) -> ServiceModel: ...
    def get_waiter_model(self, service_name: str, api_version: str | None = ...) -> WaiterModel: ...
    def get_paginator_model(
        self, service_name: str, api_version: str | None = ...
    ) -> PaginatorModel: ...
    def get_service_data(self, service_name: str, api_version: str | None = ...) -> Any: ...
    def get_available_services(self) -> Any: ...
    def set_debug_logger(self, logger_name: str = ...) -> None: ...
    def set_stream_logger(
        self,
        logger_name: str,
        log_level: str,
        stream: IO[str] | None = ...,
        format_string: str | None = ...,
    ) -> None: ...
    def set_file_logger(self, log_level: str, path: str, logger_name: str = ...) -> None: ...
    def register(
        self,
        event_name: str,
        handler: _EventHandler,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...
    def unregister(
        self,
        event_name: str,
        handler: _EventHandler | None = ...,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...
    def emit(self, event_name: str, **kwargs: Any) -> Any: ...
    def emit_first_non_none_response(self, event_name: Any, **kwargs: Any) -> Any: ...
    def get_component(self, name: Any) -> Any: ...
    def register_component(self, name: Any, component: Any) -> None: ...
    def lazy_register_component(self, name: Any, component: Any) -> None: ...
    def create_client(
        self,
        service_name: str,
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: Config | None = ...,
    ) -> BaseClient: ...
    def get_available_partitions(self) -> list[str]: ...
    def get_partition_for_region(self, region_name: str) -> str: ...
    def get_available_regions(
        self,
        service_name: str,
        partition_name: str = ...,
        allow_non_regional: bool = ...,
    ) -> list[str]: ...

class ComponentLocator:
    def __init__(self) -> None: ...
    def get_component(self, name: str) -> Any: ...
    def register_component(self, name: str, component: Any) -> None: ...
    def lazy_register_component(self, name: str, no_arg_factory: Any) -> None: ...

class SessionVarDict(MutableMapping[str, Any]):
    def __init__(self, session: Session, session_vars: Mapping[str, Any]) -> None: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...

class SubsetChainConfigFactory:
    def __init__(self, session: Session, methods: Any, environ: Any | None = ...) -> None: ...
    def create_config_chain(
        self,
        instance_name: Any | None = ...,
        env_var_names: Any | None = ...,
        config_property_name: Any | None = ...,
        default: Any | None = ...,
        conversion_func: Any | None = ...,
    ) -> Any: ...

def get_session(env_vars: dict[str, tuple[Any, Any, Any, Any]] | None = ...) -> Session: ...
