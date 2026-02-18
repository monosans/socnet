# ruff: noqa: PLC0415
from __future__ import annotations

import random
from time import perf_counter
from typing import TYPE_CHECKING, override

from django.core.management.base import BaseCommand
from django.db import transaction

if TYPE_CHECKING:
    from typing import Any

    from django.core.management.base import CommandParser


class Command(BaseCommand):
    @override
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--users", type=int, default=5000)
        parser.add_argument("--posts", type=int, default=1000000)
        parser.add_argument("--comments", type=int, default=1000000)
        parser.add_argument("--messages", type=int, default=100000)
        parser.add_argument("--subscriptions", type=int, default=100000)
        parser.add_argument("--post-likes", type=int, default=100000)
        parser.add_argument("--comment-likes", type=int, default=5000000)
        parser.add_argument("--purge", action="store_true")

    @override
    def handle(self, *args: Any, **options: Any) -> None:
        users_count: int = options["users"]
        posts_count: int = options["posts"]
        comments_count: int = options["comments"]
        messages_count: int = options["messages"]
        subscriptions_count: int = options["subscriptions"]
        post_likes_count: int = options["post_likes"]
        comment_likes_count: int = options["comment_likes"]
        purge: bool = options["purge"]

        from socnet.blog.models import Comment, Post
        from socnet.messenger.models import Message
        from socnet.users.models import User
        from tests.blog.factories import CommentFactory, PostFactory
        from tests.messenger.factories import MessageFactory
        from tests.users.factories import UserFactory

        with transaction.atomic():
            if purge:
                self.stdout.write("Purging existing data...\n\n")
                Comment.objects.all().delete()
                Post.objects.all().delete()
                Message.objects.all().delete()
                User.objects.filter(is_superuser=False).delete()

            self.stdout.write("Creating users...")
            started = perf_counter()
            users = User.objects.bulk_create(
                UserFactory.build() for _ in range(users_count)
            )
            self.stdout.write(
                f"Created {len(users):,} users"
                f" in {perf_counter() - started:,.2f} seconds."
            )

            self.stdout.write("\nCreating posts...")
            started = perf_counter()
            posts = Post.objects.bulk_create(
                PostFactory.build(author=random.choice(users))
                for _ in range(posts_count)
            )
            self.stdout.write(
                f"Created {len(posts):,} posts"
                f" in {perf_counter() - started:,.2f} seconds."
            )

            self.stdout.write("\nCreating comments...")
            started = perf_counter()
            comments = Comment.objects.bulk_create(
                CommentFactory.build(
                    post=random.choice(posts), author=random.choice(users)
                )
                for _ in range(comments_count)
            )
            self.stdout.write(
                f"Created {len(comments):,} comments"
                f" in {perf_counter() - started:,.2f} seconds."
            )

            self.stdout.write("\nCreating messages...")
            started = perf_counter()
            messages = Message.objects.bulk_create(
                MessageFactory.build(
                    sender=(u := random.choice(users)),
                    recipient=random.choice([x for x in users if x.pk != u.pk]),
                )
                for _ in range(messages_count)
            )
            self.stdout.write(
                f"Created {len(messages):,} messages"
                f" in {perf_counter() - started:,.2f} seconds."
            )

            self.stdout.write("\nCreating subscriptions...")
            started = perf_counter()
            subscriptions = User.subscriptions.through.objects.bulk_create(
                (
                    User.subscriptions.through(
                        from_user_id=(u := random.choice(users)).pk,
                        to_user_id=random.choice([
                            x for x in users if x.pk != u.pk
                        ]).pk,
                    )
                    for _ in range(subscriptions_count)
                ),
                ignore_conflicts=True,
            )
            self.stdout.write(
                f"Created {len(subscriptions):,} subscriptions"
                f" in {perf_counter() - started:,.2f} seconds."
            )
            self.stdout.write("\nCreating post likes...")
            post_likers = Post.likers.through.objects.bulk_create(
                (
                    Post.likers.through(
                        post_id=random.choice(posts).pk,
                        user_id=random.choice(users).pk,
                    )
                    for _ in range(post_likes_count)
                ),
                ignore_conflicts=True,
            )
            self.stdout.write(
                f"Created {len(post_likers):,} post likes"
                f" in {perf_counter() - started:,.2f} seconds."
            )

            self.stdout.write("\nCreating comment likes...")
            started = perf_counter()
            comment_likers = Comment.likers.through.objects.bulk_create(
                (
                    Comment.likers.through(
                        comment_id=random.choice(comments).pk,
                        user_id=random.choice(users).pk,
                    )
                    for _ in range(comment_likes_count)
                ),
                ignore_conflicts=True,
            )
            self.stdout.write(
                f"Created {len(comment_likers):,} comment likes"
                f" in {perf_counter() - started:,.2f} seconds."
            )
