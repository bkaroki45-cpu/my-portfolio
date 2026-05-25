from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import ContactMessage


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":
        form_data = {
            "name": request.POST.get("name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "subject": request.POST.get("subject", "").strip(),
            "message": request.POST.get("message", "").strip(),
        }

        if all(form_data.values()):
            ContactMessage.objects.create(**form_data)
            messages.success(request, "Thanks, your message has been sent.")
            return redirect("home")

        messages.error(request, "Please fill in every field before sending.")
        return render(request, "portfolio_app/home.html", {"form_data": form_data})

    return render(request, "portfolio_app/home.html")
