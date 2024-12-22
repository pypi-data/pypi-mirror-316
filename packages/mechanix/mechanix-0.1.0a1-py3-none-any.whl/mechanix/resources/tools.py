# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import tool_search_params, tool_summarize_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.tool_search_response import ToolSearchResponse

__all__ = ["ToolsResource", "AsyncToolsResource"]


class ToolsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#accessing-raw-response-data-eg-headers
        """
        return ToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#with_streaming_response
        """
        return ToolsResourceWithStreamingResponse(self)

    def search(
        self,
        *,
        query: str,
        x_api_key: str,
        llm_answer: bool | NotGiven = NOT_GIVEN,
        top_n: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolSearchResponse:
        """
        Search the web for a given query

        Args:
          query: The query to search for

          x_api_key: API Key for authentication

          llm_answer: Whether to return an LLM-generated answer instead of the search results

          top_n: The number of top results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"x-api-key": x_api_key, **(extra_headers or {})}
        return self._post(
            "/api/v1/tools/search",
            body=maybe_transform(
                {
                    "query": query,
                    "llm_answer": llm_answer,
                    "top_n": top_n,
                },
                tool_search_params.ToolSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ToolSearchResponse,
        )

    def summarize(
        self,
        *,
        source_type: Literal["youtube"],
        video: str,
        x_api_key: str,
        method: Literal["auto", "simple", "recursive", "multi_modal"] | NotGiven = NOT_GIVEN,
        output_language: Literal["en", "pt", "es", "it", "de", "fr"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Summarize The Contents Of The Given Source

        Args:
          video: The ID of the YouTube video to summarize. Full URLs and other forms may be
              accepted, but may not be correctly parsed.

          x_api_key: API Key for authentication

          method: The method to use for summarizing the content. Auto decides between 'simple' and
              'recursive' by length.

          output_language: The ISO 639-1 langauge code to use for the outputted summary. English (en) is
              recommended.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"x-api-key": x_api_key, **(extra_headers or {})}
        return self._post(
            "/api/v1/tools/summarize",
            body=maybe_transform(
                {
                    "source_type": source_type,
                    "video": video,
                    "method": method,
                    "output_language": output_language,
                },
                tool_summarize_params.ToolSummarizeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncToolsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mechanixlabs/python-sdk#with_streaming_response
        """
        return AsyncToolsResourceWithStreamingResponse(self)

    async def search(
        self,
        *,
        query: str,
        x_api_key: str,
        llm_answer: bool | NotGiven = NOT_GIVEN,
        top_n: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ToolSearchResponse:
        """
        Search the web for a given query

        Args:
          query: The query to search for

          x_api_key: API Key for authentication

          llm_answer: Whether to return an LLM-generated answer instead of the search results

          top_n: The number of top results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"x-api-key": x_api_key, **(extra_headers or {})}
        return await self._post(
            "/api/v1/tools/search",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "llm_answer": llm_answer,
                    "top_n": top_n,
                },
                tool_search_params.ToolSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ToolSearchResponse,
        )

    async def summarize(
        self,
        *,
        source_type: Literal["youtube"],
        video: str,
        x_api_key: str,
        method: Literal["auto", "simple", "recursive", "multi_modal"] | NotGiven = NOT_GIVEN,
        output_language: Literal["en", "pt", "es", "it", "de", "fr"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Summarize The Contents Of The Given Source

        Args:
          video: The ID of the YouTube video to summarize. Full URLs and other forms may be
              accepted, but may not be correctly parsed.

          x_api_key: API Key for authentication

          method: The method to use for summarizing the content. Auto decides between 'simple' and
              'recursive' by length.

          output_language: The ISO 639-1 langauge code to use for the outputted summary. English (en) is
              recommended.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"x-api-key": x_api_key, **(extra_headers or {})}
        return await self._post(
            "/api/v1/tools/summarize",
            body=await async_maybe_transform(
                {
                    "source_type": source_type,
                    "video": video,
                    "method": method,
                    "output_language": output_language,
                },
                tool_summarize_params.ToolSummarizeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ToolsResourceWithRawResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

        self.search = to_raw_response_wrapper(
            tools.search,
        )
        self.summarize = to_raw_response_wrapper(
            tools.summarize,
        )


class AsyncToolsResourceWithRawResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

        self.search = async_to_raw_response_wrapper(
            tools.search,
        )
        self.summarize = async_to_raw_response_wrapper(
            tools.summarize,
        )


class ToolsResourceWithStreamingResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

        self.search = to_streamed_response_wrapper(
            tools.search,
        )
        self.summarize = to_streamed_response_wrapper(
            tools.summarize,
        )


class AsyncToolsResourceWithStreamingResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

        self.search = async_to_streamed_response_wrapper(
            tools.search,
        )
        self.summarize = async_to_streamed_response_wrapper(
            tools.summarize,
        )
