from django.urls import include, path

urlpatterns = [
    path("ex00/", include("ex00.urls")),
    path("ex02/", include("ex02.urls")),
    path("ex03/", include("ex03.urls")),
    path("ex04/", include("ex04.urls")),
    path("ex05/", include("ex05.urls")),
]
