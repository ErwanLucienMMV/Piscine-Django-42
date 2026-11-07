from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    # Stop before white so all 200 cells have distinct colors across columns too.
    shades = []
    for level in range(50):
        value = level * 5
        shades.append({
            "black": f"rgb({value}, {value}, {value})",
            "red": f"rgb(255, {value}, {value})",
            "blue": f"rgb({value}, {value}, 255)",
            "green": f"rgb({value}, 255, {value})",
        })
    return render(request, "ex03/index.html", {"shades": shades})
