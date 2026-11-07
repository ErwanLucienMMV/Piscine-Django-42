from django.urls import path
from . import views

app_name = "ex07"
urlpatterns = [
    path("populate", views.populate, name="populate"),
    path("display", views.display, name="display"),
    path("update", views.update, name="update"),
]
