from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import EntryForm
from .history import append_entry, read_entries


@require_http_methods(["GET", "POST"])
def index(request):
    form = EntryForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            append_entry(form.cleaned_data["text"])
        except OSError:
            form.add_error(None, "L’entrée n’a pas pu être enregistrée. Réessayez.")
        else:
            return redirect("ex02:index")
    history_error = None
    try:
        entries = read_entries()
    except OSError:
        entries = []
        history_error = "L’historique est momentanément inaccessible. Réessayez."
    return render(request, "ex02/index.html", {
        "form": form,
        "entries": entries,
        "history_error": history_error,
    })
