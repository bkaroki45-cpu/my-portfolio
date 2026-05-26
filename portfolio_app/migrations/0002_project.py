# Generated manually on 2026-05-26

from django.db import migrations, models


PROJECTS = [
    {
        "title": "Faidi MMF",
        "status": "LIVE PROJECT",
        "featured": True,
        "highlight": "M-Pesa Integrated",
        "description": "A professional Money Market Fund (MMF) platform designed for investment management and digital financial services.",
        "features": "\n".join([
            "Secure financial workflows and backend architecture",
            "M-Pesa payment integration expertise",
            "Investment features with responsive user dashboard",
            "Modern fintech UI for digital financial services",
        ]),
        "tech_stack": "Python, Django, PostgreSQL, HTML, CSS, JavaScript",
        "categories": "Full Stack, Django, Fintech, Live Projects",
        "github_url": "https://github.com/bkaroki45-cpu/faidimmf-new.git",
        "live_url": "https://www.faidii.com/",
        "live_label": "View Live Site",
        "github_label": "GitHub Repository",
        "visual": "fintech",
        "metric": "KES",
        "sort_order": 1,
    },
    {
        "title": "TVET & Organization Voting System",
        "status": "LIVE & DEPLOYED",
        "description": "A secure online voting system designed for TVET institutions, schools, organizations, and elections management.",
        "features": "\n".join([
            "Secure authentication and admin dashboard",
            "Candidate management and election setup",
            "Live voting workflow with results management",
        ]),
        "tech_stack": "Django, Python, PostgreSQL, HTML, CSS, JavaScript",
        "categories": "Full Stack, Django, Education, Live Projects",
        "github_url": "https://github.com/bkaroki45-cpu/voting-system.git",
        "live_url": "https://voting-system-s9kz.onrender.com",
        "live_label": "Live Demo",
        "github_label": "GitHub Repo",
        "visual": "civic",
        "metric": "VOTE",
        "sort_order": 2,
    },
    {
        "title": "KaziLink",
        "status": "FULL STACK PLATFORM",
        "description": "A modern employment platform connecting employers and job seekers for every type of job opportunity.",
        "features": "\n".join([
            "Job posting and job discovery workflows",
            "Employer dashboard and applicant management",
            "User authentication with modern recruitment UI",
        ]),
        "tech_stack": "Django, PostgreSQL, JavaScript, HTML, CSS",
        "categories": "Full Stack, Django",
        "github_url": "https://github.com/bkaroki45-cpu/kazilink.git",
        "live_url": "",
        "live_label": "Live Demo",
        "github_label": "GitHub Repo",
        "visual": "recruitment",
        "metric": "JOBS",
        "sort_order": 3,
    },
    {
        "title": "MTTI ICT Feedback System",
        "status": "SYSTEM DEVELOPMENT",
        "description": "A digital feedback management system developed for educational institutions to improve communication and collect student insights efficiently.",
        "features": "\n".join([
            "Feedback submission and secure responses",
            "Structured reporting for student insights",
            "School management support workflows",
        ]),
        "tech_stack": "Django, Python, PostgreSQL, HTML, CSS",
        "categories": "Full Stack, Django, Education",
        "github_url": "https://github.com/bkaroki45-cpu/MTTI-ICT-feedback-sytem.git",
        "live_url": "",
        "live_label": "Live Demo",
        "github_label": "GitHub Repo",
        "visual": "education",
        "metric": "ICT",
        "sort_order": 4,
    },
    {
        "title": "Brian Calculator",
        "status": "FRONTEND PROJECT",
        "description": "A responsive calculator application built using frontend technologies with clean UI and interactive functionality.",
        "features": "\n".join([
            "Arithmetic calculations",
            "Responsive interface",
            "Minimal futuristic calculator preview",
        ]),
        "tech_stack": "HTML, CSS, JavaScript",
        "categories": "Frontend",
        "github_url": "https://github.com/bkaroki45-cpu/calc_brian.git",
        "live_url": "",
        "live_label": "Live Demo",
        "github_label": "GitHub Repo",
        "visual": "calculator",
        "metric": "CALC",
        "sort_order": 5,
    },
]


def seed_projects(apps, schema_editor):
    Project = apps.get_model("portfolio_app", "Project")
    for project in PROJECTS:
        Project.objects.get_or_create(title=project["title"], defaults=project)


def remove_seeded_projects(apps, schema_editor):
    Project = apps.get_model("portfolio_app", "Project")
    Project.objects.filter(title__in=[project["title"] for project in PROJECTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("status", models.CharField(default="IN DEVELOPMENT", max_length=80)),
                ("description", models.TextField()),
                ("features", models.TextField(help_text="Add one project feature per line. These appear as feature chips on the website.")),
                ("tech_stack", models.CharField(help_text="Comma-separated technologies, for example: Django, Python, PostgreSQL.", max_length=255)),
                ("categories", models.CharField(help_text="Comma-separated filters, for example: Full Stack, Django, Education. All is added automatically.", max_length=255)),
                ("github_url", models.URLField(blank=True)),
                ("live_url", models.URLField(blank=True)),
                ("github_label", models.CharField(default="GitHub Repo", max_length=60)),
                ("live_label", models.CharField(default="Live Demo", max_length=60)),
                ("visual", models.CharField(choices=[("default", "Default"), ("fintech", "Fintech"), ("civic", "Civic"), ("recruitment", "Recruitment"), ("education", "Education"), ("calculator", "Calculator")], default="default", max_length=30)),
                ("metric", models.CharField(default="APP", max_length=12)),
                ("highlight", models.CharField(blank=True, max_length=80)),
                ("featured", models.BooleanField(default=False)),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["sort_order", "title"],
            },
        ),
        migrations.RunPython(seed_projects, remove_seeded_projects),
    ]
