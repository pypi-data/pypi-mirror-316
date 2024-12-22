# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ToolSearchParams"]


class ToolSearchParams(TypedDict, total=False):
    query: Required[str]
    """The query to search for"""

    x_api_key: Required[Annotated[str, PropertyInfo(alias="x-api-key")]]
    """API Key for authentication"""

    llm_answer: bool
    """Whether to return an LLM-generated answer instead of the search results"""

    top_n: int
    """The number of top results to return"""
