from django.db import DatabaseError
from django.shortcuts import render

from .forms import SearchForm
from .models import People


def index(request):
    error = None
    try:
        genders = list(People.objects.exclude(gender__isnull=True).exclude(gender="")
                       .order_by("gender").values_list("gender", flat=True).distinct())
    except DatabaseError:
        genders = []
    if not genders:
        error = "No data available, please run: python3 manage.py load_ex10"
    form = SearchForm(request.POST if request.method == "POST" else None, genders=genders)
    rows = []
    searched = False
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        try:
            rows = list(People.objects.filter(
                gender=data["character_gender"],
                homeworld__diameter__gte=data["planet_diameter"],
                movies__release_date__range=(data["movies_minimum_release_date"],
                                            data["movies_maximum_release_date"]),
            ).order_by("movies__title", "name").values_list(
                "name", "gender", "movies__title", "homeworld__name", "homeworld__diameter",
            ))
            searched = True
        except DatabaseError:
            error = "No data available, please run: python3 manage.py load_ex10"
    return render(request, "ex10/index.html", {
        "form": form, "rows": rows, "searched": searched, "error": error,
    })
