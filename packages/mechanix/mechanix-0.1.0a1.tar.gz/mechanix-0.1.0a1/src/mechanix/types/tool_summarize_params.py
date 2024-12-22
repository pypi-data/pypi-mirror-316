# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ToolSummarizeParams"]


class ToolSummarizeParams(TypedDict, total=False):
    source_type: Required[Literal["youtube"]]

    video: Required[str]
    """The ID of the YouTube video to summarize.

    Full URLs and other forms may be accepted, but may not be correctly parsed.
    """

    x_api_key: Required[Annotated[str, PropertyInfo(alias="x-api-key")]]
    """API Key for authentication"""

    method: Literal["auto", "simple", "recursive", "multi_modal"]
    """The method to use for summarizing the content.

    Auto decides between 'simple' and 'recursive' by length.
    """

    output_language: Literal["en", "pt", "es", "it", "de", "fr"]
    """The ISO 639-1 langauge code to use for the outputted summary.

    English (en) is recommended.
    """
