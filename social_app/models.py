from django.db import models

from user.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title[:50]}..."


class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="likes", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("post", "user")

    def __str__(self):
        return f"Like on post '{self.post.title}' by {self.user.username}"
