from django.urls import path
from . import views

app_name = "ex10"
urlpatterns = [path("", views.index, name="index")]
