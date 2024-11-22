from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from socnet.core.models import MarkdownContentModel, TimestampedModel


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
    allow_commenting = models.BooleanField(
        verbose_name=_("allow commenting"),
        default=True,
        help_text=_(
            "You can comment on your posts regardless of this setting."
        ),
    )

    class Meta(TypedModelMeta):
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def get_absolute_url(self) -> str:
        return reverse("blog:post", args=(self.pk,))


class Comment(MarkdownContentModel, TimestampedModel):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("post"),
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("author"),
    )
    likers = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="liked_comments",
        verbose_name=_("likers"),
        blank=True,
    )

    class Meta(TypedModelMeta):
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def get_absolute_url(self) -> str:
        post_url = reverse("blog:post", args=(self.post_id,))
        return f"{post_url}#comment{self.pk}"
