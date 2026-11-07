from django.urls import include, path

urlpatterns = [
    path("", include("ex00.urls")),
    path("", include("ex01.urls")),
    path("", include("ex02.urls")),
    path("", include("ex03.urls")),
]
