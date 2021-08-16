from django.views.generic.edit import FormView
from literature.forms import MainSearchForm

from flb.literature.models import Article, Issue
from flb.posts.models import Post


class HomeView(FormView):
    template_name = "mainsite/home.html"
    form_class = MainSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        articles = Article.objects.all().order_by("-created_at")[:5]
        context["articles"] = articles

        posts = Post.objects.all().order_by("-created_at")[:5]
        context["posts"] = posts

        issues = Issue.objects.all().order_by("-created_at")[:5]
        context["issues"] = issues

        return context
