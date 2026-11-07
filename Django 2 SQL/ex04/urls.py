from django.urls import path
from . import views

app_name = "ex04"
urlpatterns = [
    path("init", views.init, name="init"),
    path("populate", views.populate, name="populate"),
    path("display", views.display, name="display"),
    path("remove", views.remove, name="remove"),
]
