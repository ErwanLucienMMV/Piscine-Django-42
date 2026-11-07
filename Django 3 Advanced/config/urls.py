from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from articles.views import HomeView

urlpatterns = [path("admin/", admin.site.urls), path("", HomeView.as_view(), name="root")]
urlpatterns += i18n_patterns(path("", include("articles.urls")))
