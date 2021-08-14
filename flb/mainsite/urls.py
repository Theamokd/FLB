from django.urls import path

from .views import HomeView

app_name = "mainsite"


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path('liked/', like_unlike_post, name='like-post-view'),
    # path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
]
