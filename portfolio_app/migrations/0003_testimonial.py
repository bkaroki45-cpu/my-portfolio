# Generated manually on 2026-05-26

from django.db import migrations, models


TESTIMONIALS = [
    {
        "name": "Grace Wanjiku",
        "comment": "Brian delivered a clean and reliable system. The dashboard was easy to use, and the final work felt professional from start to finish.",
        "sort_order": 1,
    },
    {
        "name": "Samuel Mwangi",
        "comment": "He understood the project quickly and built exactly what we needed. His Django work is organized, fast, and easy to maintain.",
        "sort_order": 2,
    },
    {
        "name": "Faith Njeri",
        "comment": "The website looked modern on both phone and desktop. Brian also explained the technical parts clearly, which made the process simple.",
        "sort_order": 3,
    },
    {
        "name": "Daniel Kariuki",
        "comment": "Great attention to detail. The project was completed well, the features worked smoothly, and communication was excellent.",
        "sort_order": 4,
    },
]


def seed_testimonials(apps, schema_editor):
    Testimonial = apps.get_model("portfolio_app", "Testimonial")
    for testimonial in TESTIMONIALS:
        Testimonial.objects.get_or_create(name=testimonial["name"], defaults=testimonial)


def remove_seeded_testimonials(apps, schema_editor):
    Testimonial = apps.get_model("portfolio_app", "Testimonial")
    Testimonial.objects.filter(name__in=[testimonial["name"] for testimonial in TESTIMONIALS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio_app", "0002_project"),
    ]

    operations = [
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("comment", models.TextField(help_text="What the client said about your work.")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["sort_order", "name"],
            },
        ),
        migrations.RunPython(seed_testimonials, remove_seeded_testimonials),
    ]
