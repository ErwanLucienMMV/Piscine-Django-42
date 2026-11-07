from django.urls import re_path

from . import views

app_name = "ex01"
urlpatterns = [
    re_path(r"^ex01/django/?$", views.django, name="django"),
    re_path(r"^ex01/affichage/?$", views.affichage, name="affichage"),
    re_path(r"^ex01/templates/?$", views.templates, name="templates"),
]
