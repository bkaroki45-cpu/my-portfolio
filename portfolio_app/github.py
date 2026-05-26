import json
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.cache import cache


GITHUB_API = "https://api.github.com"
CACHE_TIMEOUT = 60


def _github_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "brian-karoki-portfolio",
    }
    token = getattr(settings, "GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _fetch_json(url):
    request = Request(url, headers=_github_headers())
    with urlopen(request, timeout=6) as response:
        return json.loads(response.read().decode("utf-8"))


def _format_date(value):
    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return parsed.strftime("%b %Y")


def get_github_data():
    username = getattr(settings, "GITHUB_USERNAME", "bkaroki45-cpu")
    cache_key = f"github-data:{username}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    fallback = {
        "username": username,
        "profile_url": f"https://github.com/{username}",
        "avatar_initials": "BK",
        "public_repos": 0,
        "followers": 0,
        "total_stars": 0,
        "languages": [],
        "repos": [],
        "error": "",
    }

    try:
        profile = _fetch_json(f"{GITHUB_API}/users/{username}")
        repos = _fetch_json(
            f"{GITHUB_API}/users/{username}/repos?per_page=100&sort=updated&direction=desc&type=owner"
        )
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        fallback["error"] = str(exc)
        return fallback

    owner_repos = [repo for repo in repos if not repo.get("fork")]
    languages = sorted({repo.get("language") for repo in owner_repos if repo.get("language")})
    total_stars = sum(repo.get("stargazers_count", 0) for repo in owner_repos)
    display_repos = []

    for repo in owner_repos[:6]:
        display_repos.append(
            {
                "name": repo.get("name", ""),
                "description": repo.get("description") or "No description added yet.",
                "url": repo.get("html_url", ""),
                "language": repo.get("language") or "Code",
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "updated": _format_date(repo.get("updated_at")),
            }
        )

    data = {
        "username": profile.get("login", username),
        "profile_url": profile.get("html_url", fallback["profile_url"]),
        "avatar_initials": "".join(part[:1] for part in username.replace("-", " ").split()[:2]).upper() or "GH",
        "public_repos": profile.get("public_repos", 0),
        "followers": profile.get("followers", 0),
        "total_stars": total_stars,
        "languages": languages,
        "repos": display_repos,
        "error": "",
    }
    cache.set(cache_key, data, CACHE_TIMEOUT)
    return data
