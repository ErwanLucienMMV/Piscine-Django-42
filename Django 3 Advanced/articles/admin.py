from django.contrib import admin
from .models import Article, UserFavouriteArticle

admin.site.register(Article)
admin.site.register(UserFavouriteArticle)
