import django_filters
from fuglelittbase.literature.models import Article, Author, Issue, Journal
from taggit.models import Tag


class IssueFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Issue
        fields = [
            "name",
        ]


class ArticleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="contains")
    authors = django_filters.filters.ModelMultipleChoiceFilter(
        field_name="authors", queryset=Author.objects.all()
    )
    # We use the model tag from the taggit
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        field_name="tags", queryset=Tag.objects.all()
    )
    # We just use __ in field names to span across relationships
    journal = django_filters.ModelChoiceFilter(
        field_name="issue__journal", queryset=Journal.objects.all()
    )

    class Meta:
        model = Article
        fields = ["name", "tags", "issue__journal", "issue", "authors"]


class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="contains")

    class Meta:
        model = Author
        fields = [
            "name",
        ]
