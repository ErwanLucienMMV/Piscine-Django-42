from django.urls import path
from . import views

app_name = "ex09"
urlpatterns = [
    path("display", views.display, name="display"),
]
