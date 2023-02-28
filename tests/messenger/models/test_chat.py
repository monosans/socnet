from __future__ import annotations

import pytest

from socnet.messenger.exceptions import ChatParticipantsCountError

from ...users.factories import UserFactory
from .. import factories

factory = factories.ChatFactory


def test_chat_valid_participants_count() -> None:
    chat = factory()
    chat.participants.set((UserFactory(), UserFactory()))


@pytest.mark.parametrize("count", [1, 3])
def test_chat_creation(count: int) -> None:
    chat = factory()
    with pytest.raises(ChatParticipantsCountError):
        chat.participants.set([UserFactory() for _ in range(count)])
