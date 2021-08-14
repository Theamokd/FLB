from django.db import models
from django.urls import reverse  # just to chill pylance
from django.utils.translation import gettext as _  # just to chill pylance


class Image(models.Model):

    name = models.CharField(_("Image title"), max_length=50)
    desc = models.CharField(_("Image description"), max_length=250)
    img = models.ImageField(
        _("The image name"),
        upload_to="images",
        height_field=None,
        width_field=None,
        max_length=None,
    )
    photo_by = models.CharField(_("Photographes's name"), max_length=50, blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Image_detail", kwargs={"pk": self.pk})


class City(models.Model):

    name = models.CharField(_("City's name"), max_length=50)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Citys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("City_detail", kwargs={"pk": self.pk})


class County(models.Model):

    name = models.CharField(_("County's name"), max_length=50)

    class Meta:
        verbose_name = _("County")
        verbose_name_plural = _("Countys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("County_detail", kwargs={"pk": self.pk})


class Organization(models.Model):

    name = models.CharField(_("Organization's name"), max_length=100)
    desc = models.CharField(_("Organization's description"), max_length=250)
    county = models.ForeignKey(
        "mainsite.County",
        verbose_name=_("Journal's county"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        "mainsite.City",
        verbose_name=_("Journal's city"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organization")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Organization_detail", kwargs={"pk": self.pk})
