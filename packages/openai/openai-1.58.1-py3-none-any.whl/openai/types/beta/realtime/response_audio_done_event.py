# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["ResponseAudioDoneEvent"]


class ResponseAudioDoneEvent(BaseModel):
    content_index: int
    """The index of the content part in the item's content array."""

    event_id: str
    """The unique ID of the server event."""

    item_id: str
    """The ID of the item."""

    output_index: int
    """The index of the output item in the response."""

    response_id: str
    """The ID of the response."""

    type: Literal["response.audio.done"]
    """The event type, must be `response.audio.done`."""
