from django.db import DatabaseError, transaction
from django.http import HttpResponse
from django.shortcuts import render

from .forms import MovieForm
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
    return render(request, "ex05/messages.html", {"messages": messages})


def display(request):
    headers = [field.name for field in Movies._meta.fields]
    try:
        rows = list(Movies.objects.order_by("episode_nb").values_list(*headers))
        if rows:
            return render(request, "ex05/table.html", {"headers": headers, "rows": rows})
    except DatabaseError:
        pass
    return HttpResponse("No data available", content_type="text/plain; charset=utf-8")


def remove(request):
    try:
        titles = list(Movies.objects.order_by("episode_nb").values_list("title", flat=True))
        if not titles:
            return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
        form = MovieForm(request.POST if request.method == "POST" else None, titles=titles)
        if request.method == "POST" and form.is_valid():
            Movies.objects.filter(title=form.cleaned_data["title"]).delete()
            titles = list(Movies.objects.order_by("episode_nb").values_list("title", flat=True))
            if not titles:
                return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
            form = MovieForm(titles=titles)
    except DatabaseError:
        return HttpResponse("No data available", content_type="text/plain; charset=utf-8")
    return render(request, "ex05/form.html", {"form": form})
