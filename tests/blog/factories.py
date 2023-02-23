from __future__ import annotations

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from socnet.blog import models

from ..users.factories import UserFactory


class PostFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    text = Faker("text")

    class Meta:
        model = models.Post


class PostCommentFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    user = SubFactory(UserFactory)
    text = Faker("text")

    class Meta:
        model = models.PostComment
