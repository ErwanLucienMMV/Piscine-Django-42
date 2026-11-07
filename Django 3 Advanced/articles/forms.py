from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Article, UserFavouriteArticle


class MenuAuthenticationForm(AuthenticationForm):
    prefix = "menu"
    username = forms.CharField(label=_("Username"), widget=forms.TextInput(attrs={"placeholder": _("username"), "autocomplete": "username", "class": "form-control"}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={"placeholder": _("password"), "autocomplete": "current-password", "class": "form-control"}))


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "synopsis", "content"]
        labels = {"title": _("Title"), "synopsis": _("Synopsis"), "content": _("Content")}


class FavouriteForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteArticle
        fields = []
