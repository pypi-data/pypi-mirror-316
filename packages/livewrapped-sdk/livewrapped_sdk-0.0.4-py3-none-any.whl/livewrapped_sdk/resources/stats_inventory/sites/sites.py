#  See CONTRIBUTING.md for details.

from __future__ import annotations

from .ad_units import (
    AdUnitsResource,
    AsyncAdUnitsResource,
    AdUnitsResourceWithRawResponse,
    AsyncAdUnitsResourceWithRawResponse,
    AdUnitsResourceWithStreamingResponse,
    AsyncAdUnitsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["SitesResource", "AsyncSitesResource"]


class SitesResource(SyncAPIResource):
    @cached_property
    def ad_units(self) -> AdUnitsResource:
        return AdUnitsResource(self._client)

    @cached_property
    def with_raw_response(self) -> SitesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SitesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SitesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return SitesResourceWithStreamingResponse(self)


class AsyncSitesResource(AsyncAPIResource):
    @cached_property
    def ad_units(self) -> AsyncAdUnitsResource:
        return AsyncAdUnitsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSitesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSitesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSitesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncSitesResourceWithStreamingResponse(self)


class SitesResourceWithRawResponse:
    def __init__(self, sites: SitesResource) -> None:
        self._sites = sites

    @cached_property
    def ad_units(self) -> AdUnitsResourceWithRawResponse:
        return AdUnitsResourceWithRawResponse(self._sites.ad_units)


class AsyncSitesResourceWithRawResponse:
    def __init__(self, sites: AsyncSitesResource) -> None:
        self._sites = sites

    @cached_property
    def ad_units(self) -> AsyncAdUnitsResourceWithRawResponse:
        return AsyncAdUnitsResourceWithRawResponse(self._sites.ad_units)


class SitesResourceWithStreamingResponse:
    def __init__(self, sites: SitesResource) -> None:
        self._sites = sites

    @cached_property
    def ad_units(self) -> AdUnitsResourceWithStreamingResponse:
        return AdUnitsResourceWithStreamingResponse(self._sites.ad_units)


class AsyncSitesResourceWithStreamingResponse:
    def __init__(self, sites: AsyncSitesResource) -> None:
        self._sites = sites

    @cached_property
    def ad_units(self) -> AsyncAdUnitsResourceWithStreamingResponse:
        return AsyncAdUnitsResourceWithStreamingResponse(self._sites.ad_units)
