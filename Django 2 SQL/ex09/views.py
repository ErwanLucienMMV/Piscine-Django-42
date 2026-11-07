from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render

from .models import People


def display(request):
    try:
        rows = list(People.objects.filter(homeworld__climate__icontains="windy")
                    .order_by("name").values_list("name", "homeworld__name", "homeworld__climate"))
        if rows:
            return render(request, "ex09/table.html", {
                "headers": ["Name", "Homeworld", "Climate"], "rows": rows,
            })
    except DatabaseError:
        pass
    return HttpResponse(
        "No data available, please use the following command line before use:\n"
        "python3 manage.py load_ex09", content_type="text/plain; charset=utf-8",
    )
