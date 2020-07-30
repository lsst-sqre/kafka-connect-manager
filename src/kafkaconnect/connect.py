"""Helper class for interacting with the `Kafka Connect REST Interface
 <https://docs.confluent.io/current/connect/references/restapi.html>`_
"""

__all__ = ["Connect"]

import json
from enum import Enum
from typing import Optional

from requests import delete, get, post, put  # noqa
from requests.exceptions import ConnectionError, HTTPError


class HTTPMethod(Enum):
    """HTTP methods allowed."""

    GET = "get"
    PUT = "put"
    POST = "post"
    DELETE = "delete"


class Connect:

    _header = {"Content-Type": "application/json"}

    def __init__(self, connect_url: str) -> None:
        """Interactions with the Kafka Connect API

        Parameters
        ----------
        connect_url : `str`
            Kafka Connect URL
        """
        self._connect_url = connect_url

    def _request(
        self, method: HTTPMethod, uri: str, data: Optional[str] = None
    ) -> str:
        """Make HTTP requests.

        Parameters
        ----------
        method: `HTTPMethod`
            HTTP method as defined in the HTTPMethod class.
        uri : `str`
            The resource identifier.
        data : `str`
            The message body for the PUT request.

        Returns
        -------
        content: `ContenT` or `None`
            The response content. Returns `None` if the request was not
            successful or if the response is empty.
        """
        if method.name in ("GET", "DELETE"):
            if data:
                raise ValueError(
                    f"data argument must be None with {method.name} method."
                )
        func = eval(method.value)
        try:
            if data:
                response = func(uri, data=data, headers=Connect._header)
            else:
                response = func(uri)
            response.raise_for_status()
        except HTTPError as err:
            if err.response.status_code == 404:
                message = f"Resource {uri} not found."
                return message
            # returns 409 (Conflict) if kafka cluster rebalance is in process.
            if err.response.status_code == 409:
                message = "Kafka cluster rebalance is in process."
                return message
        except ConnectionError:
            message = (
                f"Failed to establish connection with the "
                f"Connect API {self._connect_url}."
            )
            return message
        content = ""
        if response.text:
            content = json.dumps(response.json(), indent=4, sort_keys=True)
        return content

    def list(self) -> str:
        """Get a list of active connectors."""
        uri = f"{self._connect_url}/connectors"
        return self._request(method=HTTPMethod.GET, uri=uri)

    def info(self, name: str) -> str:
        """Get information about the connector."""
        uri = f"{self._connect_url}/connectors/{name}"
        return self._request(method=HTTPMethod.GET, uri=uri)

    def status(self, name: str) -> str:
        """Get the connector status."""
        uri = f"{self._connect_url}/connectors/{name}/status"
        return self._request(method=HTTPMethod.GET, uri=uri)

    def config(self, name: str) -> str:
        """Get the connector configuration."""
        uri = f"{self._connect_url}/connectors/{name}/config"
        return self._request(method=HTTPMethod.GET, uri=uri)

    def tasks(self, name: str) -> str:
        """Get a list of tasks currently running for the connector."""
        uri = f"{self._connect_url}/connectors/{name}/tasks"
        return self._request(method=HTTPMethod.GET, uri=uri)

    def topics(self, name: str) -> str:
        """Get the list of topic names used by the connector."""
        uri = f"{self._connect_url}/connectors/{name}/topics"
        return self._request(method=HTTPMethod.GET, uri=uri)

    def plugins(self) -> str:
        """Get a list of connector plugins available in the Connect cluster."""
        uri = f"{self._connect_url}/connector-plugins"
        return self._request(method=HTTPMethod.GET, uri=uri)

    def create_or_update(self, name: str, connect_config: str) -> str:
        """Create or update a connector.

        Create a new connector using the given configuration, or update the
        configuration for an existing connector.

        Parameters
        ----------
        name : `str`
            Connector name.
        connect_config : `str`
            Connector configuration.

        Returns
        -------
        content: `ContentT` or `None`
            The response content. Returns `None` if the request was not
        successful.
        """
        uri = f"{self._connect_url}/connectors/{name}/config"
        return self._request(
            method=HTTPMethod.PUT, uri=uri, data=connect_config
        )

    def restart(self, name: str) -> str:
        """Restart the connector"""
        uri = f"{self._connect_url}/connectors/{name}/restart"
        return self._request(method=HTTPMethod.POST, uri=uri)

    def pause(self, name: str) -> str:
        """Pause the connector."""
        uri = f"{self._connect_url}/connectors/{name}/pause"
        return self._request(method=HTTPMethod.PUT, uri=uri)

    def resume(self, name: str) -> str:
        """Resume a paused connector"""
        uri = f"{self._connect_url}/connectors/{name}/resume"
        return self._request(method=HTTPMethod.PUT, uri=uri)

    def validate(self, name: str, connect_config: str) -> str:
        """Validate the connector configuration.

        Validate the configuration values against the configuration definition.
        """
        uri = f"{self._connect_url}/connector-plugins/{name}/config/validate"
        return self._request(
            method=HTTPMethod.PUT, uri=uri, data=connect_config
        )

    def remove(self, name: str) -> str:
        """Delete a connector, halting tasks and deleting its configuration."""
        uri = f"{self._connect_url}/connectors/{name}"
        return self._request(method=HTTPMethod.DELETE, uri=uri)
