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
        parser.add_argument("--users", type=int, default=10000)
        parser.add_argument("--posts-per-user", type=int, default=10)
        parser.add_argument("--comments-per-post", type=int, default=10)
        parser.add_argument("--subscriptions-per-user", type=int, default=10)
        parser.add_argument("--likes-per-post", type=int, default=10)
        parser.add_argument("--likes-per-comment", type=int, default=10)
        parser.add_argument("--messages-per-user", type=int, default=10)
        parser.add_argument("--purge", action="store_true")

    @override
    def handle(self, *args: Any, **options: Any) -> None:
        users_count: int = options["users"]
        posts_per_user: int = options["posts_per_user"]
        comments_per_post: int = options["comments_per_post"]
        messages_per_user: int = options["messages_per_user"]
        subscriptions_per_user: int = options["subscriptions_per_user"]
        likes_per_post: int = options["likes_per_post"]
        likes_per_comment: int = options["likes_per_comment"]
        purge: bool = options["purge"]

        from socnet.blog.models import Comment, Post
        from socnet.messenger.models import Message
        from socnet.users.models import User
        from tests.blog.factories import CommentFactory, PostFactory
        from tests.messenger.factories import MessageFactory
        from tests.users.factories import UserFactory

        with transaction.atomic():
            if purge:
                self.stdout.write("Purging existing data...\n")
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
                f"Created {len(users)} users"
                f" in {perf_counter() - started:,.0f} seconds."
            )

            self.stdout.write("\nCreating posts...")
            started = perf_counter()
            posts = Post.objects.bulk_create(
                PostFactory.build(author=u)
                for u in users
                for _ in range(random.randint(0, posts_per_user))
            )
            self.stdout.write(
                f"Created {len(posts)} posts"
                f" in {perf_counter() - started:,.0f} seconds."
            )

            self.stdout.write("\nCreating comments...")
            started = perf_counter()
            comments = Comment.objects.bulk_create(
                CommentFactory.build(post=p, author=random.choice(users))
                for p in posts
                for _ in range(random.randint(0, comments_per_post))
            )
            self.stdout.write(
                f"Created {len(comments)} comments"
                f" in {perf_counter() - started:,.0f} seconds."
            )

            self.stdout.write("\nCreating messages...")
            started = perf_counter()
            messages = Message.objects.bulk_create(
                MessageFactory.build(
                    sender=u,
                    recipient=random.choice([x for x in users if x.pk != u.pk]),
                )
                for u in users
                for _ in range(random.randint(0, messages_per_user))
            )
            self.stdout.write(
                f"Created {len(messages)} messages"
                f" in {perf_counter() - started:,.0f} seconds."
            )

            self.stdout.write("\nCreating subscriptions...")
            started = perf_counter()
            subscriptions = User.subscriptions.through.objects.bulk_create(
                User.subscriptions.through(
                    from_user_id=from_u.pk, to_user_id=to_u.pk
                )
                for from_u in users
                for to_u in random.sample(
                    [x for x in users if x.pk != from_u.pk],
                    random.randint(0, min(len(users), subscriptions_per_user)),
                )
            )
            self.stdout.write(
                f"Created {len(subscriptions)} subscriptions"
                f" in {perf_counter() - started:,.0f} seconds."
            )
            self.stdout.write("\nCreating post likes...")
            post_likers = Post.likers.through.objects.bulk_create(
                Post.likers.through(post_id=p.pk, user_id=u.pk)
                for p in posts
                for u in random.sample(
                    users, random.randint(0, min(len(users), likes_per_post))
                )
            )
            self.stdout.write(
                f"Created {len(post_likers)} post likes"
                f" in {perf_counter() - started:,.0f} seconds."
            )

            self.stdout.write("\nCreating comment likes...")
            started = perf_counter()
            comment_likers = Comment.likers.through.objects.bulk_create(
                Comment.likers.through(comment_id=c.pk, user_id=u.pk)
                for c in comments
                for u in random.sample(
                    users, random.randint(0, min(len(users), likes_per_comment))
                )
            )
            self.stdout.write(
                f"Created {len(comment_likers)} comment likes"
                f" in {perf_counter() - started:,.0f} seconds."
            )
