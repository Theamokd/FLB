from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from extra_views import (
    CreateWithInlinesView,
    InlineFormSetFactory,
    UpdateWithInlinesView,
)

from flb.literature.models import Article, Article_image, Author, Book, Issue, Journal

from .filters import ArticleFilter, IssueFilter
from .forms import ArticleForm, AuthorForm, IssueForm, MainSearchForm

# ********** BOOK VIEWS **********


class BookListView(ListView):
    model = Book
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book


# ********** ARTICLE VIEWS **********


class ImgArtInline(InlineFormSetFactory):
    model = Article_image
    fields = ["name", "desc", "photo_by", "img"]
    factory_kwargs = {"extra": 1}


class ArticleCreateView(CreateWithInlinesView):
    model = Article
    inlines = [
        ImgArtInline,
    ]
    form_class = ArticleForm

    # Custom to add the single formset for crispy as inline_formset.
    def get_context_data(self, **kwargs):
        data = super(ArticleCreateView, self).get_context_data(**kwargs)

        inline_instance = ImgArtInline(
            self.model, self.request, self.object, self.kwargs
        )
        data["inline_formset"] = inline_instance.construct_formset()

        return data

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        issue = Issue.objects.get(pk=self.kwargs["pk"])
        obj.issue = issue
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(UpdateWithInlinesView):
    model = Article
    inlines = [
        ImgArtInline,
    ]
    form_class = ArticleForm

    # Custom  to return the single formset for crispy
    def get_context_data(self, **kwargs):
        data = super(ArticleUpdateView, self).get_context_data(**kwargs)

        inline_instance = ImgArtInline(
            self.model, self.request, self.object, self.kwargs
        )
        data["inline_formset"] = inline_instance.construct_formset()

        return data

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)


class ArticleDetailView(DetailView):
    model = Article


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "snippets/confirm_delete.html"
    success_url = reverse_lazy("base")
    # To add loginmixin and editor check


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtered_articles = ArticleFilter(
            self.request.GET,
        )
        context["filtered_articles"] = filtered_articles

        return context


# ********** JOURNAL VIEWS **********


class JournalDetailView(DetailView):
    model = Journal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        issues = self.object.issue_set.all()
        context["issues"] = issues
        issues_filtered_list = IssueFilter(self.request.GET, queryset=issues)
        context["filtered_issues"] = issues_filtered_list

        articles = Article.objects.filter(issue__journal=self.object)
        context["articles"] = articles

        authors = Author.objects.filter(authors__issue__journal=self.object).distinct
        context["authors"] = authors

        return context


class JournalListView(ListView):
    model = Journal
    # paginate_by = 10


# ********** ISSUE VIEWS **********


class IssueDetailView(DetailView):
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()

        articles = self.object.article_set.all()
        context["articles"] = articles

        authors = Author.objects.filter(authors__issue=self.object).distinct
        context["authors"] = authors

        return context


class IssueCreateView(CreateView):
    model = Issue
    form_class = IssueForm

    def get_form_kwargs(self):
        kwargs = super(IssueCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(IssueCreateView, self).form_valid(form)

    # To add loginmixin and editor check


class IssueUpdateView(UpdateView):
    model = Issue
    form_class = IssueForm

    def get_form_kwargs(self):
        kwargs = super(IssueUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    # To add loginmixin and editor check


class IssueDeleteView(DeleteView):
    model = Issue
    template_name = "snippets/confirm_delete.html"
    success_url = reverse_lazy("literature:journal-list")
    # To add loginmixin and editor check


# ********** AUTHOR VIEWS **********


class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()

        articles = Article.objects.filter(authors=self.object)
        context["articles"] = articles

        return context


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse("<script> window.close(); </script>")


class AuthorUpdateView(UpdateView):
    model = Author
    fields = ("first_name", "last_name", "org")


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = "snippets/confirm_delete.html"


class SearchView(FormView):
    template_name = "literature/search.html"
    form_class = MainSearchForm

    def get_initial(self):
        initial = super(SearchView, self).get_initial()
        initial.update(self.request.GET.items())
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        request = self.request

        # Getting query param from GET
        query = request.GET.get("q", None)

        # Filtering the context objects by query
        if query is not None:
            articles = (
                Article.objects.search(query)
                .select_related("issue", "issue__journal")
                .prefetch_related(
                    "authors",
                    "tags",
                )
            )
            books = Book.objects.search(query).prefetch_related(
                "authors",
                "tags",
            )
        else:
            articles = (
                Article.objects.all()
                .select_related("issue", "issue__journal")
                .prefetch_related(
                    "authors",
                    "tags",
                )
            )
            books = Book.objects.all().prefetch_related(
                "authors",
                "tags",
            )

        # Filter by file
        file = request.GET.get("file", None)
        if file is not None:
            articles = articles.exclude(file="")
            books = books.exclude(file="")

        # Filter by tags
        get_tags = request.GET.getlist("tags", None)
        if get_tags:
            articles = articles.filter(tags__name__in=get_tags)
            books = books.filter(tags__name__in=get_tags)

        # Filter by journal
        get_journals = request.GET.getlist("journals", None)
        if get_journals:
            articles = articles.filter(issue__journal__name__in=get_journals)

        # Filter by authors
        get_authors = request.GET.getlist("authors", None)
        if get_authors:
            articles = articles.filter(authors__name__in=get_authors)
            books = books.filter(authors__name__in=get_authors)

        # Filter by years
        get_years = request.GET.getlist("years", None)
        if get_years:
            articles = articles.filter(issue__date__year__in=get_years)
            books = books.filter(date__year__in=get_years)

        # Setting the filters value after filtering
        article_tags = list(articles.values_list("tags__name", flat=True))
        book_tags = list(books.values_list("tags__name", flat=True))
        tags = set(article_tags + book_tags)

        journals = set(articles.values_list("issue__journal__name", flat=True))

        article_authors = list(articles.values_list("authors__name", flat=True))
        book_authors = list(books.values_list("authors__name", flat=True))
        authors = set(article_authors + book_authors)

        article_years = list(articles.values_list("issue__date__year", flat=True))
        book_years = list(books.values_list("date__year", flat=True))
        years = set(article_years + book_years)

        # Making sure there are no duplicates
        articles = articles.distinct()
        books = books.distinct()

        # Setting the pagination
        articles_paginator = Paginator(articles, 10)
        a_page_number = request.GET.get("a-page")
        paged_articles = articles_paginator.get_page(a_page_number)
        context["paged_articles"] = paged_articles

        books_paginator = Paginator(books, 10)
        b_page_number = request.GET.get("b-page")
        paged_books = books_paginator.get_page(b_page_number)
        context["paged_books"] = paged_books

        # Setting the counts
        context["articles_count"] = articles.count()
        context["books_count"] = books.count()

        # Setting the params in context
        context["query"] = query
        context["get_years"] = get_years
        context["years"] = years
        context["file"] = file
        context["get_tags"] = get_tags
        context["tags"] = tags
        context["authors"] = authors
        context["get_authors"] = get_authors
        context["journals"] = journals
        context["get_journals"] = get_journals

        context["request"] = request

        # context['form'] = form

        return context
