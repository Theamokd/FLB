from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    AuthorCreateView,
    AuthorDeleteView,
    AuthorDetailView,
    AuthorUpdateView,
    BookDetailView,
    BookListView,
    IssueCreateView,
    IssueDeleteView,
    IssueDetailView,
    IssueUpdateView,
    JournalDetailView,
    JournalListView,
    SearchView,
)

app_name = "literature"


urlpatterns = [
    path("journals/", JournalListView.as_view(), name="journal-list"),
    path("journals/<slug:slug>/", JournalDetailView.as_view(), name="journal-detail"),
    path("issue/create/", IssueCreateView.as_view(), name="issue-create"),
    path("issue/<pk>/update/", IssueUpdateView.as_view(), name="issue-update"),
    path("issue/<pk>/delete/", IssueDeleteView.as_view(), name="issue-delete"),
    path("issue/<slug:slug>/", IssueDetailView.as_view(), name="issue-detail"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("article/create/<pk>/", ArticleCreateView.as_view(), name="article-create"),
    path("article/<pk>/update/", ArticleUpdateView.as_view(), name="article-update"),
    path("article/<pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("book/<slug:slug>/", BookDetailView.as_view(), name="book-detail"),
    path("author/create/", AuthorCreateView.as_view(), name="author-create"),
    path("author/<pk>/update/", AuthorUpdateView.as_view(), name="author-update"),
    path("author/<pk>/delete/", AuthorDeleteView.as_view(), name="author-delete"),
    path("author/<slug:slug>/", AuthorDetailView.as_view(), name="author-detail"),
    path("search/", SearchView.as_view(), name="search"),
]
