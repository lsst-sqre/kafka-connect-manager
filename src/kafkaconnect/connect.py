"""Helper class for interacting with the `Kafka Connect REST Interface
 <https://docs.confluent.io/current/connect/references/restapi.html#put--connectors-(string-name)-config>`_
"""

__all__ = ["Connect"]

import json
import logging

import requests
from requests.exceptions import ConnectionError, HTTPError

logger = logging.getLogger("connect")


class Connect:

    _header = {"Content-Type": "application/json"}

    def __init__(self, connect_url: str) -> None:
        self._connect_url = connect_url

    def _get(self, uri: str) -> str:
        """HTTP GET request.

        Parameters
        ----------
        uri : `str`
            The resource identifier.

        Returns
        -------
        content : `str`
            The response content.
        """
        try:
            response = requests.get(uri)
            response.raise_for_status()
        except HTTPError as err:
            if err.response.status_code == 404:
                message = f"Resource {uri} not found."
                logger.error(message)
            raise
        except ConnectionError:
            message = (
                f"Failed to establish connection with {self._connect_url}."
            )
            logger.error(message)
            raise
        content = json.dumps(response.json(), indent=4, sort_keys=True)
        return content

    def list(self) -> str:
        """Get a list of active connectors."""
        uri = f"{self._connect_url}/connectors"
        return self._get(uri)

    def info(self, name: str) -> str:
        """Get information about the connector."""
        uri = f"{self._connect_url}/connectors/{name}"
        return self._get(uri)

    def status(self, name: str) -> str:
        """Get the connector status."""
        uri = f"{self._connect_url}/connectors/{name}/status"
        return self._get(uri)

    def config(self, name: str) -> str:
        """Get the connector configuration."""
        uri = f"{self._connect_url}/connectors/{name}/config"
        return self._get(uri)

    def tasks(self, name: str) -> str:
        """Get a list of tasks currently running for the connector."""
        uri = f"{self._connect_url}/connectors/{name}/tasks"
        return self._get(uri)

    def topics(self, name: str) -> str:
        """Get the list of topic names used by the connector."""
        uri = f"{self._connect_url}/connectors/{name}/topics"
        return self._get(uri)

    def plugins(self) -> str:
        """Get a list of connector plugins available in the Connect cluster."""
        uri = f"{self._connect_url}/connector-plugis"
        return self._get(uri)

