#!/usr/bin/env python3
"""Refresh only curated public repositories; keep committed data on API failure."""
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import tomllib
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+")


def normalize(repo, payload):
    if not isinstance(payload, dict) or payload.get("full_name", "").lower() != repo.lower():
        raise ValueError("unexpected repository response")
    if payload.get("private") is not False:
        raise ValueError("only public repositories may be displayed")
    result = {"repo": repo, "html_url": "https://github.com/" + repo}
    for field in ("description", "language", "homepage", "pushed_at", "default_branch"):
        value = payload.get(field)
        if value is not None and not isinstance(value, str):
            raise ValueError("invalid metadata field: " + field)
        result[field] = value or ""
    if result["pushed_at"]:
        datetime.fromisoformat(result["pushed_at"].replace("Z", "+00:00"))
    stars = payload.get("stargazers_count", 0)
    if type(stars) is not int or stars < 0:
        raise ValueError("invalid star count")
    result["stars"] = stars
    return result


def fetch_repo(repo):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "manxisuo-blog-projects", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request("https://api.github.com/repos/" + repo, headers=headers)
    with urlopen(request, timeout=8) as response:
        body = response.read(1_000_001)
    if len(body) > 1_000_000:
        raise ValueError("repository response too large")
    return json.loads(body)


def sync(config_path, output_path, fetch=fetch_repo):
    with config_path.open("rb") as handle:
        items = tomllib.load(handle).get("items", [])
    repos = [item["repo"] for item in items]
    if not repos or len(repos) != len(set(repos)) or any(not REPO_PATTERN.fullmatch(repo) for repo in repos):
        raise ValueError("project list must contain unique owner/repository names")
    cached = json.loads(output_path.read_text(encoding="utf-8")) if output_path.exists() else {}
    if not isinstance(cached, dict):
        raise ValueError("cached metadata must be an object")
    result = {}
    for repo in repos:
        try:
            result[repo] = normalize(repo, fetch(repo))
            print("Updated " + repo)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
            # Never log response bodies or headers: they may contain credentials.
            status = "HTTP " + str(error.code) if isinstance(error, HTTPError) else type(error).__name__
            if isinstance(cached.get(repo), dict):
                result[repo] = cached[repo]
                print("Warning: " + repo + " (" + status + "); using saved metadata", file=sys.stderr)
            else:
                print("Warning: " + repo + " (" + status + "); metadata unavailable", file=sys.stderr)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output_path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    try:
        temporary.replace(output_path)
    finally:
        temporary.unlink(missing_ok=True)
    return result


if __name__ == "__main__":
    sync(ROOT / "data/projects.toml", ROOT / "data/github_projects.json")
