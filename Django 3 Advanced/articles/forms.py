from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Article, UserFavouriteArticle


class MenuAuthenticationForm(AuthenticationForm):
    prefix = "menu"
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "username", "autocomplete": "username"}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={"placeholder": "password", "autocomplete": "current-password"}))


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "synopsis", "content"]


class FavouriteForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteArticle
        fields = []
