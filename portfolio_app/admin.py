from django.contrib import admin

from .models import ContactMessage, Project, Testimonial


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "featured", "is_published", "sort_order")
    list_editable = ("featured", "is_published", "sort_order")
    list_filter = ("featured", "is_published", "visual")
    search_fields = ("title", "description", "tech_stack", "categories")
    fieldsets = (
        (
            "Project Details",
            {
                "fields": (
                    "title",
                    "status",
                    "description",
                    "highlight",
                    "featured",
                    "is_published",
                    "sort_order",
                )
            },
        ),
        ("Card Content", {"fields": ("features", "tech_stack", "categories", "visual", "metric")}),
        ("Links", {"fields": ("github_url", "github_label", "live_url", "live_label")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "sort_order", "created_at")
    list_editable = ("is_published", "sort_order")
    search_fields = ("name", "comment")
    list_filter = ("is_published",)
    readonly_fields = ("created_at",)
