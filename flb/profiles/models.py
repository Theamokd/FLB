from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _  # just to chill pylance


# Here we can extend with all the info we need about the profile
class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        _("Image"),
        upload_to="profiles",
        blank=True,
        null=True,
        default="defaults/default-journal.png",
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%d-%m-%Y')}"

    __initial_first_name = None
    __initial_last_name = None

    # Override init method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def get_absolute_url(self):
        return reverse("profiles:profile-detail", kwargs={"pk": self.pk})
