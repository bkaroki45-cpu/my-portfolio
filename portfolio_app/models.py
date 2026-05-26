from django.db import models


class Project(models.Model):
    VISUAL_CHOICES = [
        ("default", "Default"),
        ("fintech", "Fintech"),
        ("civic", "Civic"),
        ("recruitment", "Recruitment"),
        ("education", "Education"),
        ("calculator", "Calculator"),
    ]

    title = models.CharField(max_length=160)
    status = models.CharField(max_length=80, default="IN DEVELOPMENT")
    description = models.TextField()
    features = models.TextField(
        help_text="Add one project feature per line. These appear as feature chips on the website."
    )
    tech_stack = models.CharField(
        max_length=255,
        help_text="Comma-separated technologies, for example: Django, Python, PostgreSQL.",
    )
    categories = models.CharField(
        max_length=255,
        help_text="Comma-separated filters, for example: Full Stack, Django, Education. All is added automatically.",
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    github_label = models.CharField(max_length=60, default="GitHub Repo")
    live_label = models.CharField(max_length=60, default="Live Demo")
    visual = models.CharField(max_length=30, choices=VISUAL_CHOICES, default="default")
    metric = models.CharField(max_length=12, default="APP")
    highlight = models.CharField(max_length=80, blank=True)
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title

    def _split_lines(self, value):
        return [item.strip() for item in value.splitlines() if item.strip()]

    def _split_csv(self, value):
        return [item.strip() for item in value.split(",") if item.strip()]

    def category_list(self):
        categories = self._split_csv(self.categories)
        return ["All", *[category for category in categories if category != "All"]]

    def to_card_data(self):
        return {
            "title": self.title,
            "status": self.status,
            "featured": self.featured,
            "highlight": self.highlight,
            "description": self.description,
            "features": self._split_lines(self.features),
            "techStack": self._split_csv(self.tech_stack),
            "categories": self.category_list(),
            "github": self.github_url,
            "live": self.live_url,
            "liveLabel": self.live_label,
            "githubLabel": self.github_label,
            "visual": self.visual,
            "metric": self.metric,
        }


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    comment = models.TextField(help_text="What the client said about your work.")
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name
