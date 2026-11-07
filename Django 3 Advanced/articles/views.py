from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView, ListView, RedirectView
from .models import Article, UserFavouriteArticle


class HomeView(RedirectView):
    pattern_name = "articles"
    permanent = False


class ArticleListView(ListView):
    model = Article
    template_name = "articles/articles.html"
    context_object_name = "articles"

    def get_queryset(self):
        return super().get_queryset().select_related("author")


class PublicationListView(LoginRequiredMixin, ArticleListView):
    template_name = "articles/publications.html"

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"


class FavouriteListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = "articles/favourites.html"
    context_object_name = "favourites"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).select_related("article")


class ArticleLoginView(LoginView):
    template_name = "articles/login.html"


class ArticleLogoutView(LogoutView):
    pass
