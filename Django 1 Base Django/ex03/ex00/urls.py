from django.urls import re_path

from . import views

app_name = "ex00"
urlpatterns = [re_path(r"^ex00/?$", views.index, name="index")]
