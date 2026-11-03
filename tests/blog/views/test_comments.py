from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse

from tests.blog import factories
from tests.utils import auth_client, parametrize_by_auth, set_image

if TYPE_CHECKING:
    from django.test import Client

    from socnet.blog import models

factory = factories.CommentFactory


def get_url(post: models.Post) -> str:
    return reverse("blog:comments", args=(post.pk,))


def test_non_htmx(client: Client) -> None:
    post = factories.PostFactory.create()
    factory.create(post=post)
    response = client.get(get_url(post))
    assert response.status_code == 400


@parametrize_by_auth
def test_lists_only_post_comments(client: Client, *, auth: bool) -> None:
    if auth:
        auth_client(client)
    post = factories.PostFactory.create()
    comments = factory.create_batch(2, post=post)
    other_comment = factory.create()
    response = client.get(get_url(post), headers={"hx-request": "true"})
    assert response.status_code == 200
    assert list(response.context["comments"]) == comments
    content = response.content.decode()
    for comment in comments:
        assert f'id="comment{comment.pk}"' in content
    assert f'id="comment{other_comment.pk}"' not in content


def test_pagination(client: Client) -> None:
    post = factories.PostFactory.create()
    comments = factory.create_batch(11, post=post)
    url = get_url(post)
    response = client.get(url, headers={"hx-request": "true"})
    assert response.status_code == 200
    assert list(response.context["comments"]) == comments[:10]
    assert 'hx-get="?page=2"' in response.content.decode()
    response = client.get(url, data={"page": 2}, headers={"hx-request": "true"})
    assert response.status_code == 200
    assert list(response.context["comments"]) == comments[10:]
    assert "hx-get" not in response.content.decode()


def test_unauthed_likes_link_to_login(client: Client) -> None:
    comment = factory.create()
    comment.likers.add(comment.author)
    url = get_url(comment.post)
    response = client.get(url, headers={"hx-request": "true"})
    assert response.status_code == 200
    [rendered] = response.context["comments"]
    assert rendered.likers__count == 1
    content = response.content.decode()
    assert "{}?next={}".format(reverse("account_login"), url) in content
    assert "data-comment-pk" not in content


def test_is_liked(client: Client) -> None:
    user = auth_client(client)
    post = factories.PostFactory.create()
    liked, _ = factory.create_batch(2, post=post)
    liked.likers.add(user)
    response = client.get(get_url(post), headers={"hx-request": "true"})
    assert response.status_code == 200
    assert [c.is_liked for c in response.context["comments"]] == [True, False]
    content = response.content.decode()
    assert content.count('data-is-liked="y"') == 1
    assert content.count('data-is-liked="n"') == 1


def test_controls_for_comment_author(client: Client) -> None:
    user = auth_client(client)
    comment = factory.create(author=user)
    response = client.get(get_url(comment.post), headers={"hx-request": "true"})
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("blog:comment_update", args=(comment.pk,)) in content
    assert reverse("blog:comment_delete", args=(comment.pk,)) in content
    assert reverse("admin:blog_comment_change", args=(comment.pk,)) not in content


def test_controls_for_post_author(client: Client) -> None:
    user = auth_client(client)
    post = factories.PostFactory.create(author=user)
    comment = factory.create(post=post)
    response = client.get(get_url(post), headers={"hx-request": "true"})
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("blog:comment_update", args=(comment.pk,)) not in content
    assert reverse("blog:comment_delete", args=(comment.pk,)) in content


def test_controls_for_other_user(client: Client) -> None:
    auth_client(client)
    comment = factory.create()
    response = client.get(get_url(comment.post), headers={"hx-request": "true"})
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("blog:comment_update", args=(comment.pk,)) not in content
    assert reverse("blog:comment_delete", args=(comment.pk,)) not in content


def test_controls_for_staff(admin_client: Client) -> None:
    comment = factory.create()
    response = admin_client.get(get_url(comment.post), headers={"hx-request": "true"})
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("admin:blog_comment_change", args=(comment.pk,)) in content
    assert reverse("blog:comment_update", args=(comment.pk,)) not in content
    assert reverse("blog:comment_delete", args=(comment.pk,)) not in content


def test_author_image(client: Client) -> None:
    comment = factory.create()
    image_src = set_image(comment.author)
    response = client.get(get_url(comment.post), headers={"hx-request": "true"})
    assert response.status_code == 200
    assert image_src in response.content.decode()
