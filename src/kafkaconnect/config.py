"""Kafkaconnect and connector configuration."""

__all__ = ["Config", "ConnectorConfig"]

import abc
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class Config:
    """Application configuration."""

    broker_url: str
    """The Kafka Broker URL.
    """

    connect_url: str
    """The Kafka Connect URL.

    The Kafka Connect REST API is used to manage connectors.
    """

    sasl_plain_username: Optional[str] = None
    """Username for SASL authentication.
       If specified then you must also specify sasl_plain_password.
       Default: None
    """

    sasl_plain_password: Optional[str] = None
    """Password for SASL authentication.
       If specified then you must also specify sasl_plain_username.
       Default: None
    """

    def __post_init__(self) -> None:
        """Post init validation."""
        if (self.sasl_plain_username is None) != (
            self.sasl_plain_password is None
        ):
            raise ValueError(
                "Both or neither of 'sasl_plain_username' "
                "and 'sasl_plain_password' must be specified."
            )


class ConnectorConfig(metaclass=abc.ABCMeta):
    """Connector configuration interface."""

    def __subclasshook__(cls, subclass: Any) -> bool:
        """Make sure the abstract method is overriden in the subclass."""
        return (
            hasattr(subclass, "update_topics")
            and callable(subclass.update_topics)
            or NotImplemented
        )

    @abc.abstractmethod
    def update_topics(self, topics: Set[str]) -> None:
        """update_topics() abstract method."""
        raise NotImplementedError

    @staticmethod
    def format_field_names(fields: List[Tuple[str, Any]]) -> Dict[str, str]:
        """Rename a field name by replacing '_' with '.'.

        Dictionary factory used with the dataclasses.asdict() method.
        """
        result = []
        for f in fields:
            name, value = f
            name = name.replace("_", ".")
            result.append((name, value))
        return dict(result)

    def asjson(self) -> str:
        """Convert dataclass instance into JSON."""
        config = asdict(self, dict_factory=self.format_field_names)
        return json.dumps(config, indent=4, sort_keys=True)
