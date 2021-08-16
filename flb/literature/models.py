from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse  # just to chill pylance
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.translation import gettext as _  # just to chill pylance
from taggit.managers import TaggableManager


# The manager for searching after a keyword
class BookManager(models.Manager):
    # Search by keyword method
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            if query.isdigit():
                or_lookup = (
                    Q(name__icontains=query)
                    | Q(date__year=query)
                    | Q(authors__first_name__icontains=query)
                    | Q(authors__last_name__icontains=query)
                    | Q(authors__name__icontains=query)
                    | Q(tags__name__in=[query])
                )
            else:
                or_lookup = (
                    Q(name__icontains=query)
                    | Q(authors__first_name__icontains=query)
                    | Q(authors__last_name__icontains=query)
                    | Q(authors__name__icontains=query)
                    | Q(tags__name__in=[query])
                )
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Book(models.Model):

    name = models.CharField(_("Book title"), max_length=50)
    slug = models.SlugField(_("Book Slug"), max_length=255, unique=True, blank=True)
    desc = models.TextField(_("Book description"), blank=True)
    link = models.CharField(_("Link to book"), max_length=150, blank=True)
    created_at = models.DateTimeField(
        _("Uploaded on"), auto_now=False, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Changed on"), auto_now=True, auto_now_add=False
    )
    f_cover = models.ImageField(
        _("The front cover image"),
        upload_to="files/books/covers",
        blank=True,
        null=True,
        default="files/defaults/default-journal.png",
    )
    b_cover = models.ImageField(
        _("The back cover image"), upload_to="files/books/covers", blank=True, null=True
    )
    volume = models.SmallIntegerField(_("Volume number"), blank=True, null=True)
    date = models.DateField(
        _("Publishing date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    issn = models.CharField(_("ISSN number"), max_length=50, blank=True)
    file = models.FileField(
        _("The Issue file (pdf)"), upload_to="files/books", blank=True
    )
    tags = TaggableManager(
        blank=True,
    )

    custom_txt = models.CharField(_("Custom text"), max_length=350, blank=True)
    custom_num = models.IntegerField(_("Custom number"), blank=True, null=True)
    custom_bool = models.BooleanField(_("Custom bool"), default=False)

    authors = models.ManyToManyField(
        "literature.Author",
        verbose_name=_("Books's authors"),
        related_name="books_authors",
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="bok_creators",
        verbose_name=_("Book creator"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = BookManager()

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ["-date", "name"]

        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "desc",
                ]
            ),
            models.Index(
                fields=[
                    "date",
                ]
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name + "-" + get_random_string(8, "0123456789"))
        return super().save(*args, **kwargs)

    def slug_title(self):
        return slugify(self.name)

    # To get the model name in the search template
    def model_name(self):
        return self.__class__.__name__


class JournalManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            qs = qs.filter(
                name__icontains=query
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Journal(models.Model):
    name = models.CharField(_("Journal name"), max_length=150)
    slug = models.SlugField(_("Journal Slug"), max_length=255, unique=True, blank=True)
    desc = models.TextField(_("Journal description"), blank=True)
    link = models.CharField(_("Link to journal"), max_length=150, blank=True)
    created_at = models.DateTimeField(
        _("Uploaded on"), auto_now=False, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Changed on"), auto_now=True, auto_now_add=False
    )
    f_cover = models.ImageField(
        _("The front cover image"),
        upload_to="files/journals/covers",
        blank=True,
        default="files/defaults/default-journal.png",
    )
    b_cover = models.ImageField(
        _("The back cover image"),
        upload_to="files/journals/covers",
        blank=True,
        null=True,
    )

    custom_txt = models.CharField(_("Custom text"), max_length=350, blank=True)
    custom_num = models.IntegerField(_("Custom number"), blank=True, null=True)
    custom_bool = models.BooleanField(_("Custom bool"), default=False)

    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("Editors of the journal"), blank=True
    )
    publisher = models.ForeignKey(
        "mainsite.Organization",
        verbose_name=_("Journal's publisher"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
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

    objects = JournalManager()

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")
        ordering = ["name"]

        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "desc",
                ]
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name + "-" + get_random_string(8, "0123456789"))
        return super().save(*args, **kwargs)

    def slug_title(self):
        return slugify(self.name)

    # To get the model name in the search template
    def model_name(self):
        return self.__class__.__name__


class IssueManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            if query.isdigit():
                or_lookup = Q(name__icontains=query) | Q(date__year=query)
            else:
                or_lookup = Q(name__icontains=query)
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Issue(models.Model):
    name = models.CharField(_("Issue name"), max_length=150)
    slug = models.SlugField(_("Issue Slug"), max_length=255, unique=True, blank=True)
    volume = models.SmallIntegerField(_("Volume number"), blank=True, null=True)
    date = models.DateField(
        _("Publishing date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    issn = models.CharField(_("ISSN number"), max_length=50, blank=True)
    file = models.FileField(
        _("The Issue file (pdf)"), upload_to="files/issues", blank=True
    )
    desc = models.TextField(_("Issue description"), blank=True)
    link = models.CharField(_("Link to journal"), max_length=150, blank=True)
    created_at = models.DateTimeField(
        _("Uploaded on"), auto_now=False, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Changed on"), auto_now=True, auto_now_add=False
    )
    f_cover = models.ImageField(
        _("The front cover image"),
        upload_to="files/issues/covers",
        blank=True,
        default="files/defaults/default-issue.png",
    )
    b_cover = models.ImageField(
        _("The back cover image"), upload_to="files/issues/covers", blank=True
    )

    custom_txt = models.CharField(_("Custom text"), max_length=350, blank=True)
    custom_num = models.IntegerField(_("Custom number"), blank=True, null=True)
    custom_bool = models.BooleanField(_("Custom bool"), default=False)

    redactor = models.ForeignKey(
        "literature.Author",
        verbose_name=_("The redactor of the issue"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    journal = models.ForeignKey(
        "literature.Journal",
        verbose_name=_("Issue's journal"),
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="iss_creators",
        verbose_name=_("Issue creator"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = IssueManager()

    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")
        ordering = ["-date", "name"]

        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "date",
                ]
            ),
            models.Index(
                fields=[
                    "journal",
                ]
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name + "-" + get_random_string(8, "0123456789"))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("literature:issue-update", kwargs={"pk": self.pk})

    # To get the model name in the search template
    def model_name(self):
        return self.__class__.__name__


class ArticleManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            if query.isdigit():
                or_lookup = (
                    Q(name__icontains=query)
                    | Q(abstract__icontains=query)
                    | Q(issue__date__year=query)
                    | Q(authors__first_name__icontains=query)
                    | Q(authors__last_name__icontains=query)
                    | Q(authors__name__icontains=query)
                    | Q(tags__name__in=[query])
                )
            else:
                or_lookup = (
                    Q(name__icontains=query)
                    | Q(abstract__icontains=query)
                    | Q(authors__first_name__icontains=query)
                    | Q(authors__last_name__icontains=query)
                    | Q(authors__name__icontains=query)
                    | Q(tags__name__in=[query])
                )
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Article(models.Model):
    name = models.CharField(_("Article's title"), max_length=150)
    slug = models.SlugField(_("Article Slug"), max_length=255, unique=True, blank=True)
    sub = models.CharField(_("Article's subtitle"), max_length=250, blank=True)
    abstract = models.TextField(_("Article's abstract"), blank=True)
    text = models.TextField(_("Article's text"), blank=True)
    file = models.FileField(_("Article's file"), upload_to="files/articles", blank=True)
    link = models.CharField(_("Link to article"), max_length=150, blank=True)
    tags = TaggableManager(blank=True)

    created_at = models.DateTimeField(
        _("Uploaded on"), auto_now=False, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Changed on"), auto_now=True, auto_now_add=False
    )

    custom_txt = models.CharField(_("Custom text"), max_length=350, blank=True)
    custom_num = models.IntegerField(_("Custom number"), blank=True, null=True)
    custom_bool = models.BooleanField(_("Custom bool"), default=False)

    authors = models.ManyToManyField(
        "literature.Author",
        verbose_name=_("Article's authors"),
        related_name="authors",
        blank=True,
    )
    issue = models.ForeignKey(
        "literature.Issue", verbose_name=_("Issue"), on_delete=models.CASCADE, null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="art_creators",
        verbose_name=_("Article creator"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = ArticleManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ["-issue__date", "name"]

        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "abstract",
                ]
            ),
            models.Index(
                fields=[
                    "issue",
                ]
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name + "-" + get_random_string(8, "0123456789"))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("literature:article-update", kwargs={"pk": self.pk})

    # To get the model name in the search template
    def model_name(self):
        return self.__class__.__name__


class Article_image(models.Model):

    name = models.CharField(_("Image title"), max_length=50, blank=True)
    desc = models.CharField(_("Image description"), max_length=250, blank=True)
    img = models.ImageField(_("The image name"), upload_to="article_images")
    photo_by = models.CharField(_("Photographers's name"), max_length=50, blank=True)

    article = models.ForeignKey(
        "literature.Article",
        verbose_name=_("Related article"),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name


class Author(models.Model):

    name = models.CharField(_("Author's full name"), max_length=100, blank=True)
    first_name = models.CharField(_("Author's first name"), max_length=50)
    last_name = models.CharField(_("Author's last name"), max_length=50)
    slug = models.SlugField(_("Author Slug"), max_length=255, unique=True, blank=True)
    org = models.ForeignKey(
        "mainsite.Organization",
        verbose_name=_("Author's organization"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Related user"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
        ordering = ["name"]

        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "first_name",
                ]
            ),
            models.Index(
                fields=[
                    "last_name",
                ]
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(
                self.first_name
                + "-"
                + self.last_name
                + "-"
                + get_random_string(8, "0123456789")
            )
        if not self.name:
            self.name = self.first_name + " " + self.last_name
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("literature:author-update", kwargs={"pk": self.pk})
