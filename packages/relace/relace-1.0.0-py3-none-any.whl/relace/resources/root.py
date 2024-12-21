# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.root_hello_response import RootHelloResponse

__all__ = ["RootResource", "AsyncRootResource"]


class RootResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RootResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/squack-io/relace-python#accessing-raw-response-data-eg-headers
        """
        return RootResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RootResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/squack-io/relace-python#with_streaming_response
        """
        return RootResourceWithStreamingResponse(self)

    def hello(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RootHelloResponse:
        """Return a friendly hello message."""
        return self._get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RootHelloResponse,
        )


class AsyncRootResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRootResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/squack-io/relace-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRootResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRootResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/squack-io/relace-python#with_streaming_response
        """
        return AsyncRootResourceWithStreamingResponse(self)

    async def hello(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RootHelloResponse:
        """Return a friendly hello message."""
        return await self._get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RootHelloResponse,
        )


class RootResourceWithRawResponse:
    def __init__(self, root: RootResource) -> None:
        self._root = root

        self.hello = to_raw_response_wrapper(
            root.hello,
        )


class AsyncRootResourceWithRawResponse:
    def __init__(self, root: AsyncRootResource) -> None:
        self._root = root

        self.hello = async_to_raw_response_wrapper(
            root.hello,
        )


class RootResourceWithStreamingResponse:
    def __init__(self, root: RootResource) -> None:
        self._root = root

        self.hello = to_streamed_response_wrapper(
            root.hello,
        )


class AsyncRootResourceWithStreamingResponse:
    def __init__(self, root: AsyncRootResource) -> None:
        self._root = root

        self.hello = async_to_streamed_response_wrapper(
            root.hello,
        )
