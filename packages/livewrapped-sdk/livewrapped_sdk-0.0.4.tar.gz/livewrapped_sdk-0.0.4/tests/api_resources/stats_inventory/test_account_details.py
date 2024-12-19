#  See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from livewrapped_sdk import LivewrappedSDK, AsyncLivewrappedSDK
from livewrapped_sdk.types.stats_inventory import AccountDetails

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccountDetails:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: LivewrappedSDK) -> None:
        account_detail = client.stats_inventory.account_details.retrieve()
        assert_matches_type(AccountDetails, account_detail, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: LivewrappedSDK) -> None:
        response = client.stats_inventory.account_details.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account_detail = response.parse()
        assert_matches_type(AccountDetails, account_detail, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: LivewrappedSDK) -> None:
        with client.stats_inventory.account_details.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account_detail = response.parse()
            assert_matches_type(AccountDetails, account_detail, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAccountDetails:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLivewrappedSDK) -> None:
        account_detail = await async_client.stats_inventory.account_details.retrieve()
        assert_matches_type(AccountDetails, account_detail, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLivewrappedSDK) -> None:
        response = await async_client.stats_inventory.account_details.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account_detail = await response.parse()
        assert_matches_type(AccountDetails, account_detail, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLivewrappedSDK) -> None:
        async with async_client.stats_inventory.account_details.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account_detail = await response.parse()
            assert_matches_type(AccountDetails, account_detail, path=["response"])

        assert cast(Any, response.is_closed) is True
