from __future__ import annotations

from io import StringIO

from django.core.management import call_command
from django.db.models import F

from socnet.blog.models import Comment, Post
from socnet.messenger.models import Message
from socnet.users.models import User
from tests.blog.factories import CommentFactory
from tests.messenger.factories import MessageFactory
from tests.users.factories import UserFactory

COUNTS = {
    "users": 3,
    "posts": 4,
    "comments": 5,
    "messages": 6,
    "subscriptions": 7,
    "post_likes": 8,
    "comment_likes": 9,
}


def mock_data(**options: object) -> str:
    stdout = StringIO()
    call_command("mock_data", **COUNTS, **options, stdout=stdout)
    return stdout.getvalue()


def test_mock_data() -> None:
    output = mock_data()
    assert User.objects.count() == 3
    assert Post.objects.count() == 4
    assert Comment.objects.count() == 5
    assert Message.objects.count() == 6
    assert not Message.objects.filter(sender=F("recipient")).exists()
    # Duplicates are dropped, so there may be fewer of these than requested.
    subscriptions = User.subscriptions.through.objects
    assert 1 <= subscriptions.count() <= 6
    assert not subscriptions.filter(from_user=F("to_user")).exists()
    assert 1 <= Post.likers.through.objects.count() <= 8
    assert 1 <= Comment.likers.through.objects.count() <= 9
    assert "Created 3 users" in output
    assert "Purging" not in output


def test_mock_data_purge() -> None:
    admin = UserFactory.create(is_superuser=True)
    CommentFactory.create()
    MessageFactory.create()
    output = mock_data(purge=True)
    assert "Purging existing data..." in output
    assert User.objects.count() == 4
    assert User.objects.filter(pk=admin.pk).exists()
    assert Post.objects.count() == 4
    assert Comment.objects.count() == 5
    assert Message.objects.count() == 6


def test_mock_data_keeps_existing_data() -> None:
    CommentFactory.create()
    mock_data()
    assert Post.objects.count() == 5
    assert Comment.objects.count() == 6


def test_mock_data_again_in_a_new_process() -> None:
    UserFactory.create(username="USER_4")
    # Each run is a new process, which starts the factory's numbering from 0.
    UserFactory.reset_sequence()
    mock_data()
    UserFactory.reset_sequence()
    mock_data()
    assert User.objects.count() == 7
    assert Post.objects.count() == 8
