from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _

from ..core.fields import NormalizedTextField


class Post(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("user"),
    )
    text = NormalizedTextField(
        verbose_name=_("text"), max_length=4096, blank=True
    )
    image = models.ImageField(
        verbose_name=_("image"), upload_to="post_images/%Y/%m/%d/", blank=True
    )
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

    def clean(self) -> None:
        if not self.text and not self.image:
            raise ValidationError(
                gettext("You must provide either text or an image"),
                code="must_provide_either_text_or_image",
            )


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
    text = NormalizedTextField(
        verbose_name=_("text"), max_length=4096, blank=True
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to="post_comment_images/%Y/%m/%d/",
        blank=True,
    )
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

    def clean(self) -> None:
        if not self.text and not self.image:
            raise ValidationError(
                gettext("You must provide either text or an image"),
                code="must_provide_either_text_or_image",
            )
