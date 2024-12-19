#  See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from livewrapped_sdk import LivewrappedSDK, AsyncLivewrappedSDK

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccount:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_login(self, client: LivewrappedSDK) -> None:
        account = client.account.login(
            email="x",
            password="x",
        )
        assert_matches_type(str, account, path=["response"])

    @parametrize
    def test_raw_response_login(self, client: LivewrappedSDK) -> None:
        response = client.account.with_raw_response.login(
            email="x",
            password="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(str, account, path=["response"])

    @parametrize
    def test_streaming_response_login(self, client: LivewrappedSDK) -> None:
        with client.account.with_streaming_response.login(
            email="x",
            password="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(str, account, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAccount:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_login(self, async_client: AsyncLivewrappedSDK) -> None:
        account = await async_client.account.login(
            email="x",
            password="x",
        )
        assert_matches_type(str, account, path=["response"])

    @parametrize
    async def test_raw_response_login(self, async_client: AsyncLivewrappedSDK) -> None:
        response = await async_client.account.with_raw_response.login(
            email="x",
            password="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(str, account, path=["response"])

    @parametrize
    async def test_streaming_response_login(self, async_client: AsyncLivewrappedSDK) -> None:
        async with async_client.account.with_streaming_response.login(
            email="x",
            password="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(str, account, path=["response"])

        assert cast(Any, response.is_closed) is True
