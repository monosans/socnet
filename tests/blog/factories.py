from __future__ import annotations

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from socnet.blog import models
from tests.users.factories import UserFactory


class PostFactory(DjangoModelFactory):
    author = SubFactory(UserFactory)
    content = Faker("text")

    class Meta:
        model = models.Post


class CommentFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    author = SubFactory(UserFactory)
    content = Faker("text")

    class Meta:
        model = models.Comment
