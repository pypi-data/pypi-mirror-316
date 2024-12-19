#  See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from livewrapped_sdk import LivewrappedSDK, AsyncLivewrappedSDK
from livewrapped_sdk.types.stats_inventory import BuyerMinimal

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBuyers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: LivewrappedSDK) -> None:
        buyer = client.stats_inventory.buyers.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BuyerMinimal, buyer, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: LivewrappedSDK) -> None:
        response = client.stats_inventory.buyers.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        buyer = response.parse()
        assert_matches_type(BuyerMinimal, buyer, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: LivewrappedSDK) -> None:
        with client.stats_inventory.buyers.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            buyer = response.parse()
            assert_matches_type(BuyerMinimal, buyer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: LivewrappedSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `buyer_id` but received ''"):
            client.stats_inventory.buyers.with_raw_response.retrieve(
                "",
            )


class TestAsyncBuyers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLivewrappedSDK) -> None:
        buyer = await async_client.stats_inventory.buyers.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BuyerMinimal, buyer, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLivewrappedSDK) -> None:
        response = await async_client.stats_inventory.buyers.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        buyer = await response.parse()
        assert_matches_type(BuyerMinimal, buyer, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLivewrappedSDK) -> None:
        async with async_client.stats_inventory.buyers.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            buyer = await response.parse()
            assert_matches_type(BuyerMinimal, buyer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLivewrappedSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `buyer_id` but received ''"):
            await async_client.stats_inventory.buyers.with_raw_response.retrieve(
                "",
            )
