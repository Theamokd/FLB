from django.db import models
from django.urls.base import reverse
from django.utils.translation import gettext as _


class Post(models.Model):
    name = models.CharField(_("Title"), max_length=50)
    text = models.TextField(_("Text"))
    image = models.ImageField(
        _("Post image"),
        upload_to="posts",
        blank=True,
        default="defaults/default-news.png",
    )
    created_at = models.DateTimeField(
        _("Uploaded on"), auto_now=False, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Changed on"), auto_now=True, auto_now_add=False
    )
    author = models.CharField(_("Post author"), max_length=50)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Post_detail", kwargs={"pk": self.pk})
