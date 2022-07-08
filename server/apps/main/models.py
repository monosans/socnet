from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import datetime
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


def upload_date() -> str:
    today = datetime.today()
    return f"{today.year}/{today.month}/{today.day}"


def post_image(instance: "Post", filename: str) -> str:
    return f"user_{instance.user_id}/posts/{upload_date()}/{filename}"


class Post(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("user"),
    )
    text = models.TextField(
        verbose_name=_("text"), max_length=4096, blank=True
    )
    image = models.ImageField(
        verbose_name=_("image"), upload_to=post_image, blank=True
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
        ordering = ("-pk",)

    def get_absolute_url(self) -> str:
        return reverse("post", args=(self.pk,))

    def clean(self) -> None:
        if not self.text and not self.image:
            raise ValidationError(
                gettext("You must provide either text or an image")
            )


def post_comment_image(instance: "PostComment", filename: str) -> str:
    return f"user_{instance.user_id}/comments/{upload_date()}/{filename}"


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
    text = models.TextField(
        verbose_name=_("text"), max_length=4096, blank=True
    )
    image = models.ImageField(
        verbose_name=_("image"), upload_to=post_comment_image, blank=True
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
                gettext("You must provide either text or an image")
            )
