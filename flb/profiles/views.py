from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from fuglelittbase.literature.models import Journal
from fuglelittbase.profiles.models import Profile

from .forms import ProfileForm


class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        journals = Journal.objects.filter(editors=self.object.user)
        context["journals"] = journals

        return context


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
