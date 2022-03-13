import logging

from httpx import Client, Timeout, HTTPStatusError, TransportError

from djstarter import decorators

logger = logging.getLogger(__name__)

TIMEOUT = Timeout(connect=5, read=10, write=5, pool=5)
RETRY_EXCEPTIONS = (
    HTTPStatusError,
    TransportError
)


class Http2Client(Client):
    """
    Http/2 Client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            follow_redirects=True,
            headers=self.init_headers(),
            http2=True,
            timeout=TIMEOUT,
            *args,
            **kwargs
        )

    @staticmethod
    def init_headers():
        return {
            'accept': 'application/json',
        }

    @decorators.retry(retry_exceptions=RETRY_EXCEPTIONS)
    @decorators.api_error_check
    def send(self, *args, **kwargs):
        return super().send(*args, **kwargs)
