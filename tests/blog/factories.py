from __future__ import annotations

from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker

from socnet.blog import models
from tests.users.factories import UserFactory


class PostFactory(DjangoModelFactory[models.Post]):
    author = SubFactory(UserFactory)
    content = Faker("text")

    class Meta:
        model = models.Post


class CommentFactory(DjangoModelFactory[models.Comment]):
    post = SubFactory(PostFactory)
    author = SubFactory(UserFactory)
    content = Faker("text")

    class Meta:
        model = models.Comment
