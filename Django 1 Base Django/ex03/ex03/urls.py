from django.urls import re_path

from . import views

app_name = "ex03"
urlpatterns = [re_path(r"^ex03/?$", views.index, name="index")]
