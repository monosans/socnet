from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from . import forms


@require_http_methods(["GET", "POST"])
def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = forms.UserCreationForm()
    context = {"form": form}
    return render(request, "users/register.html", context)
