# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mechanix import Mechanix, AsyncMechanix
from tests.utils import assert_matches_type
from mechanix.types import ToolSearchResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTools:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_search(self, client: Mechanix) -> None:
        tool = client.tools.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
        )
        assert_matches_type(ToolSearchResponse, tool, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: Mechanix) -> None:
        tool = client.tools.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
            llm_answer=True,
            top_n=1,
        )
        assert_matches_type(ToolSearchResponse, tool, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: Mechanix) -> None:
        response = client.tools.with_raw_response.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(ToolSearchResponse, tool, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: Mechanix) -> None:
        with client.tools.with_streaming_response.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(ToolSearchResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_summarize(self, client: Mechanix) -> None:
        tool = client.tools.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
        )
        assert_matches_type(object, tool, path=["response"])

    @parametrize
    def test_method_summarize_with_all_params(self, client: Mechanix) -> None:
        tool = client.tools.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
            method="auto",
            output_language="en",
        )
        assert_matches_type(object, tool, path=["response"])

    @parametrize
    def test_raw_response_summarize(self, client: Mechanix) -> None:
        response = client.tools.with_raw_response.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(object, tool, path=["response"])

    @parametrize
    def test_streaming_response_summarize(self, client: Mechanix) -> None:
        with client.tools.with_streaming_response.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(object, tool, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTools:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_search(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
        )
        assert_matches_type(ToolSearchResponse, tool, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
            llm_answer=True,
            top_n=1,
        )
        assert_matches_type(ToolSearchResponse, tool, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncMechanix) -> None:
        response = await async_client.tools.with_raw_response.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(ToolSearchResponse, tool, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncMechanix) -> None:
        async with async_client.tools.with_streaming_response.search(
            query="Common organelles within a human eukaryote",
            x_api_key="x-api-key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(ToolSearchResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_summarize(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
        )
        assert_matches_type(object, tool, path=["response"])

    @parametrize
    async def test_method_summarize_with_all_params(self, async_client: AsyncMechanix) -> None:
        tool = await async_client.tools.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
            method="auto",
            output_language="en",
        )
        assert_matches_type(object, tool, path=["response"])

    @parametrize
    async def test_raw_response_summarize(self, async_client: AsyncMechanix) -> None:
        response = await async_client.tools.with_raw_response.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(object, tool, path=["response"])

    @parametrize
    async def test_streaming_response_summarize(self, async_client: AsyncMechanix) -> None:
        async with async_client.tools.with_streaming_response.summarize(
            source_type="youtube",
            video="5qSrmeiWsuc",
            x_api_key="x-api-key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(object, tool, path=["response"])

        assert cast(Any, response.is_closed) is True
