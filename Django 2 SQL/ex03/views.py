from django.db import DatabaseError, transaction
from django.http import HttpResponse
from django.shortcuts import render

from .data import MOVIES
from .models import Movies


def populate(request):
    messages = []
    for movie in MOVIES:
        try:
            with transaction.atomic():
                Movies.objects.create(**movie)
            messages.append("OK")
        except DatabaseError as error:
            messages.append(f"{movie['title']}: {error}")
    return render(request, "ex03/messages.html", {"messages": messages})


def display(request):
    headers = [field.name for field in Movies._meta.fields]
    try:
        rows = list(Movies.objects.order_by("episode_nb").values_list(*headers))
        if rows:
            return render(request, "ex03/table.html", {"headers": headers, "rows": rows})
    except DatabaseError:
        pass
    return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
