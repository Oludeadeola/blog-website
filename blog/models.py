from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _

from auths.models import Blogger
from commons.models import AbstractCommonModel


# Create your models here


class Post(AbstractCommonModel):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")
        REMOVED = "removed", _("Removed")

    title = models.CharField(verbose_name=_("Title"), max_length=255)
    body = models.TextField(verbose_name=_("Body"))
    number_of_likes = models.IntegerField(verbose_name=_("Number Of Likes"), default=0)
    blogger = models.ForeignKey(
        verbose_name=_("Blogger"),
        to=Blogger,
        on_delete=CASCADE,
        related_name="posts",
    )
    status = models.CharField(
        verbose_name=_("Status"), choices=Status.choices, default=Status.DRAFT
    )

    def __str__(self) -> str:
        return f"{self.title} - {self.blogger.first_name} {self.blogger.last_name}"


class Media(AbstractCommonModel):
    cloud_url = models.URLField()
    post = models.ForeignKey(
        verbose_name=_("Post"), to=Post, on_delete=CASCADE, related_name="medias"
    )

    def __str__(self) -> str:
        return f"{self.post.title} - {self.cloud_url}"


class Comment(AbstractCommonModel):
    author = models.ForeignKey(verbose_name=_("Author"), to=Blogger, on_delete=CASCADE)
    post = models.ForeignKey(
        verbose_name=_("Post"), to=Post, on_delete=CASCADE, related_name="comments"
    )
    body = models.TextField(verbose_name=_("Body"))
    is_deleted = models.BooleanField(verbose_name=_("Deleted"), default=False)

    def __str__(self) -> str:
        return f"{self.author.username}'s comment on {self.post.blogger.username}'s post - {self.post.title}"


class Like(AbstractCommonModel):
    post = models.ForeignKey(
        verbose_name=_("Post"), to=Post, on_delete=CASCADE, related_name="likes"
    )
    creator = models.ForeignKey(
        verbose_name=_("Creator"), to=Blogger, on_delete=CASCADE
    )

    def __str__(self) -> str:
        return f"{self.post.title} - {self.post.number_of_likes}"


class Tag(AbstractCommonModel):
    name = models.CharField(verbose_name=_("Tag"), unique=True)
    posts = models.ManyToManyField(
        verbose_name=_("Posts"), to=Post, related_name="tags", related_query_name="tag"
    )

    def __str__(self):
        return f"{self.name}"


class Category(AbstractCommonModel):
    name = models.CharField(verbose_name=_("Category"), unique=True)
    posts = models.ManyToManyField(
        verbose_name=_("Posts"), to=Post, related_name="category"
    )

    def __str__(self):
        return f"{self.name}"
