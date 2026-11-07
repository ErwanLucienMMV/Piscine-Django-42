from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, RedirectView
from .forms import ArticleForm, FavouriteForm, MenuAuthenticationForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["favourite_form"] = FavouriteForm(instance=UserFavouriteArticle(article=self.object))
            context["is_favourite"] = UserFavouriteArticle.objects.filter(user=self.request.user, article=self.object).exists()
        return context


class FavouriteListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = "articles/favourites.html"
    context_object_name = "favourites"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).select_related("article")


class ArticleLoginView(LoginView):
    template_name = "articles/login.html"
    authentication_form = MenuAuthenticationForm

    def get_success_url(self):
        return reverse("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = context["form"]
        return context


class ArticleLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "articles/form.html"
    success_url = reverse_lazy("login")
    extra_context = {"heading": _("Register")}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)


class PublishView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/form.html"
    extra_context = {"heading": _("Publish")}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    form_class = FavouriteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = UserFavouriteArticle(article=get_object_or_404(Article, pk=self.kwargs["pk"]))
        return kwargs

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs["pk"])
        return HttpResponseRedirect(article.get_absolute_url())

    def form_valid(self, form):
        self.object, _ = UserFavouriteArticle.objects.get_or_create(user=self.request.user, article=form.instance.article)
        return HttpResponseRedirect(self.object.article.get_absolute_url())
