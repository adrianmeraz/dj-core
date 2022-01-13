from unittest.mock import Mock

import httpx
from django.test import TestCase
from httpx import Request, Response
from rest_framework import status

from core import decorators, exceptions


class DecoratorTests(TestCase):
    """
    Decorator Tests
    """

    def test_retry(self):
        tries = 5
        func = Mock(side_effect=exceptions.ApiError("Test"))
        decorated_function = decorators.retry(
            retry_exceptions=(exceptions.ApiError,),
            tries=tries,
            delay=0,
            backoff=1,
            jitter=0,
        )(func)
        with self.assertRaises(exceptions.ApiError):
            decorated_function()
        self.assertEquals(func.call_count, tries)

    def test_check_response_400(self):
        request = Request(url='', method='')
        func = Mock(side_effect=httpx.HTTPStatusError(
            request=request,
            response=Response(
                request=request,
                status_code=status.HTTP_400_BAD_REQUEST,
            ),
            message='test'
        ))
        decorated_function = decorators.api_error_check(func)
        with self.assertRaises(exceptions.ApiError):
            decorated_function()

    def test_check_response_502(self):
        request = Request(url='', method='')
        func = Mock(side_effect=httpx.HTTPStatusError(
            request=request,
            response=Response(
                request=request,
                status_code=status.HTTP_502_BAD_GATEWAY,
            ),
            message='test'
        ))
        decorated_function = decorators.api_error_check(func)
        with self.assertRaises(httpx.HTTPStatusError):
            decorated_function()

    def test_delay_fn(self):
        def double(x): return 2 * x
        decorated_function = decorators.delay_fn(seconds=0)(double)
        self.assertEquals(decorated_function(31), 62)
