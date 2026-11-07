def make_urlpatterns():
    from django.urls import path
    from .views import hello_world

    return [path("helloworld", hello_world, name="hello_world")]


urlpatterns = make_urlpatterns()
