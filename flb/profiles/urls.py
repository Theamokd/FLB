from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView

app_name = "profiles"

urlpatterns = [
    path("profile/<pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("update/<pk>/", ProfileUpdateView.as_view(), name="profile-update"),
]
