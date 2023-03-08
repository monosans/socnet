from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..core.models import MarkdownContentModel, TimestampedModel


class Post(MarkdownContentModel, TimestampedModel):
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("author"),
    )
    likers = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        verbose_name=_("likers"),
        blank=True,
    )

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def get_absolute_url(self) -> str:
        return reverse("blog:post", args=(self.pk,))


class PostComment(MarkdownContentModel, TimestampedModel):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("post"),
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_comments",
        verbose_name=_("author"),
    )
    likers = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="liked_comments",
        verbose_name=_("likers"),
        blank=True,
    )

    class Meta:
        verbose_name = _("post comment")
        verbose_name_plural = _("post comments")

    def get_absolute_url(self) -> str:
        post_url = reverse("blog:post", args=(self.post_id,))
        return f"{post_url}#comment{self.pk}"
