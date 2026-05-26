from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .github import get_github_data
from .models import ContactMessage, Project, Testimonial


def get_home_context(extra_context=None):
    projects = Project.objects.filter(is_published=True)
    testimonials = Testimonial.objects.filter(is_published=True)
    context = {
        "github": get_github_data(),
        "project_cards": [project.to_card_data() for project in projects],
        "testimonials": testimonials,
    }
    if extra_context:
        context.update(extra_context)
    return context


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
        return render(request, "portfolio_app/home.html", get_home_context({"form_data": form_data}))

    return render(request, "portfolio_app/home.html", get_home_context())
