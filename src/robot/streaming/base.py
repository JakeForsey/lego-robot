from abc import ABC, abstractmethod
import logging
import socket

LOGGER = logging.getLogger(__name__)


class StreamBase(ABC):

    def __init__(self, hivemind_ip: str, port: int):
        self._hivemind_ip = hivemind_ip
        self._port = port

    def __enter__(self):
        try:
            self._client_socket = socket.socket()
            self._client_socket.connect((self._hivemind_ip, self._port))
        except socket.error:
            LOGGER.warn("Unable to connect to hivemind at ip: %s, port: %s", self._hivemind_ip, self._port)

        self._on_enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client_socket.close()
        self._on_exit()

    def get_socket(self):
        return self._client_socket

    @abstractmethod
    def _on_enter(self):
        pass

    @abstractmethod
    def _on_exit(self):
        pass

    @abstractmethod
    async def stream(self):
        pass
