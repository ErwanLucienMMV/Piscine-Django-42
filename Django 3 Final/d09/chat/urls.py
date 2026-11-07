from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("", views.rooms, name="rooms"),
    path("<int:room_id>/", views.room, name="room"),
]
