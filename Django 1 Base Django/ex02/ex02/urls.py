from django.urls import re_path

from . import views

app_name = "ex02"
urlpatterns = [re_path(r"^ex02/?$", views.index, name="index")]
