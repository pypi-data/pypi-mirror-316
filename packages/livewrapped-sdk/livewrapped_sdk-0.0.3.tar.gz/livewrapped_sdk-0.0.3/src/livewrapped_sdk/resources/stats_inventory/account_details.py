#  See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.stats_inventory.account_details import AccountDetails

__all__ = ["AccountDetailsResource", "AsyncAccountDetailsResource"]


class AccountDetailsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AccountDetailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AccountDetailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccountDetailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AccountDetailsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountDetails:
        """
        Retrieves all buyers, publishers and if there is one, the master publisher
        connected to the logged in user. Information is abbreviated and contains only id
        and name.
        """
        return self._get(
            "/StatsInventory/accountdetails",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountDetails,
        )


class AsyncAccountDetailsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAccountDetailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAccountDetailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccountDetailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncAccountDetailsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountDetails:
        """
        Retrieves all buyers, publishers and if there is one, the master publisher
        connected to the logged in user. Information is abbreviated and contains only id
        and name.
        """
        return await self._get(
            "/StatsInventory/accountdetails",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountDetails,
        )


class AccountDetailsResourceWithRawResponse:
    def __init__(self, account_details: AccountDetailsResource) -> None:
        self._account_details = account_details

        self.retrieve = to_raw_response_wrapper(
            account_details.retrieve,
        )


class AsyncAccountDetailsResourceWithRawResponse:
    def __init__(self, account_details: AsyncAccountDetailsResource) -> None:
        self._account_details = account_details

        self.retrieve = async_to_raw_response_wrapper(
            account_details.retrieve,
        )


class AccountDetailsResourceWithStreamingResponse:
    def __init__(self, account_details: AccountDetailsResource) -> None:
        self._account_details = account_details

        self.retrieve = to_streamed_response_wrapper(
            account_details.retrieve,
        )


class AsyncAccountDetailsResourceWithStreamingResponse:
    def __init__(self, account_details: AsyncAccountDetailsResource) -> None:
        self._account_details = account_details

        self.retrieve = async_to_streamed_response_wrapper(
            account_details.retrieve,
        )
