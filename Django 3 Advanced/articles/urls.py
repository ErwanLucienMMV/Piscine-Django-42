from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("articles", views.ArticleListView.as_view(), name="articles"),
    path("login", views.ArticleLoginView.as_view(), name="login"),
    path("logout", views.ArticleLogoutView.as_view(), name="logout"),
    path("publications", views.PublicationListView.as_view(), name="publications"),
    path("favourites", views.FavouriteListView.as_view(), name="favourites"),
    path("articles/<int:pk>", views.ArticleDetailView.as_view(), name="detail"),
]
