from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _


class Post(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("user"),
    )
    text = models.TextField(verbose_name=_("text"), max_length=4096)
    date = models.DateTimeField(verbose_name=_("date/time"), auto_now_add=True)
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


class PostComment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("post"),
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_comments",
        verbose_name=_("user"),
    )
    text = models.TextField(verbose_name=_("text"), max_length=4096)
    date = models.DateTimeField(verbose_name=_("date/time"), auto_now_add=True)
    likers = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="liked_comments",
        verbose_name=_("likers"),
        blank=True,
    )

    class Meta:
        verbose_name = _("post comment")
        verbose_name_plural = _("post comments")
