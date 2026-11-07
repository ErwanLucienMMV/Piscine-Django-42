from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Room


@login_required
def rooms(request):
    return render(request, "chat/rooms.html", {"rooms": Room.objects.all()})


@login_required
def room(request, room_id):
    return render(request, "chat/room.html", {"room": get_object_or_404(Room, pk=room_id)})
