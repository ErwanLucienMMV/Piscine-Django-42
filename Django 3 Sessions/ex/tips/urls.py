from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("tips/<int:pk>/vote/<str:direction>/", views.vote, name="vote"),
    path("tips/<int:pk>/delete/", views.delete_tip, name="delete_tip"),
]
