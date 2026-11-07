from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def django(request):
    return render(request, "ex01/django.html")


@require_GET
def affichage(request):
    return render(request, "ex01/affichage.html")


@require_GET
def templates(request):
    return render(request, "ex01/templates.html", {
        "visitor": "lectrice ou lecteur",
        "topics": ["Héritage", "Boucles", "Conditions", "Variables"],
        "show_example": True,
    })
