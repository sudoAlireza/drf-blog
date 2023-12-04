from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Rating(models.Model):
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name="ratings", on_delete=models.CASCADE, default=0
    )

    rate = models.IntegerField(choices=[(i, str(i)) for i in range(6)])

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f"{self.user.username} - {self.post.title}: {self.rate}"
