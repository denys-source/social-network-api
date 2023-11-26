from urllib.parse import urljoin

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework_simplejwt.authentication import get_user_model

from social_app.models import Post
from social_app.serializers import PostSerializer


POSTS_URL = reverse("social_app:posts-list")


def post_detail_url(pk: int) -> str:
    return reverse("social_app:posts-detail", kwargs={"pk": pk})


class PostViewSetTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.force_authenticate(self.user)
        self.post_data = {"title": "test_title", "text": "test_body"}

    def _create_post(self) -> Post:
        return self.client.post(POSTS_URL, data=self.post_data)

    def test_list_posts(self) -> None:
        resp = self.client.get(POSTS_URL)
        self.assertEqual(resp.status_code, 200)

    def test_create_post_success(self) -> None:
        resp = self._create_post()
        created_post = Post.objects.first()
        serializer = PostSerializer(created_post)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)

        for key, value in self.post_data.items():
            self.assertEqual(value, serializer.data.get(key))

    def test_create_post_failure(self) -> None:
        resp = self.client.post(POSTS_URL)
        self.assertEqual(resp.status_code, 400)

    def test_like_post(self) -> None:
        self._create_post()

        url = urljoin(post_detail_url(pk=1), "like/")
        resp = self.client.post(url)
        post = Post.objects.first()

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(post.likes.count(), 1)

    def test_multiple_likes_single_post(self) -> None:
        self._create_post()

        url = urljoin(post_detail_url(pk=1), "like/")
        self.client.post(url)
        resp = self.client.post(url)
        post = Post.objects.first()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(post.likes.count(), 1)

    def test_unlike_post(self) -> None:
        self._create_post()

        like_url = urljoin(post_detail_url(pk=1), "like/")
        unlike_url = urljoin(post_detail_url(pk=1), "unlike/")
        self.client.post(like_url)
        resp = self.client.post(unlike_url)
        post = Post.objects.first()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(post.likes.count(), 0)

    def test_multiple_unlikes_single_post(self) -> None:
        self._create_post()

        like_url = urljoin(post_detail_url(pk=1), "like/")
        unlike_url = urljoin(post_detail_url(pk=1), "unlike/")
        self.client.post(like_url)
        self.client.post(unlike_url)
        resp = self.client.post(unlike_url)
        post = Post.objects.first()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(post.likes.count(), 0)
