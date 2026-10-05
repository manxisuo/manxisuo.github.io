import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location("sync_projects", Path(__file__).resolve().parents[1] / "scripts/sync_projects.py")
sync_projects = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_projects)


class ProjectSyncTests(unittest.TestCase):
    def test_allowlist_refresh_and_per_repo_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            config, output = Path(folder) / "projects.toml", Path(folder) / "cache.json"
            config.write_text('[[items]]\nrepo="owner/first"\n[[items]]\nrepo="owner/second"\n')
            previous = {"owner/second": {"language": "Go", "stars": 2}, "owner/unlisted": {"stars": 99}}
            output.write_text(json.dumps(previous))
            requested = []
            def fetch(repo):
                requested.append(repo)
                if repo.endswith("second"):
                    raise HTTPError("https://api.github.com", 403, "limited", {}, None)
                return {"full_name": repo, "private": False, "language": "Python", "stargazers_count": 3}
            result = sync_projects.sync(config, output, fetch)
            self.assertEqual(requested, ["owner/first", "owner/second"])
            self.assertEqual(result["owner/first"]["stars"], 3)
            self.assertEqual(result["owner/second"], previous["owner/second"])
            self.assertNotIn("owner/unlisted", result)
            self.assertEqual(json.loads(output.read_text()), result)

    def test_invalid_response_keeps_cache(self):
        with tempfile.TemporaryDirectory() as folder:
            config, output = Path(folder) / "projects.toml", Path(folder) / "cache.json"
            config.write_text('[[items]]\nrepo="owner/first"\n')
            cached = {"owner/first": {"language": "Go"}}
            output.write_text(json.dumps(cached))
            result = sync_projects.sync(config, output, lambda _: {"full_name": "other/repo", "private": False})
            self.assertEqual(result, cached)

    def test_private_or_invalid_date_metadata_is_rejected(self):
        for payload in [
            {"full_name": "owner/first", "private": True},
            {"full_name": "owner/first", "private": False, "pushed_at": "not a date"},
        ]:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                sync_projects.normalize("owner/first", payload)

    def test_invalid_repo_is_rejected_before_network(self):
        with tempfile.TemporaryDirectory() as folder:
            config, output = Path(folder) / "projects.toml", Path(folder) / "cache.json"
            config.write_text('[[items]]\nrepo="owner/repo?token=bad"\n')
            with self.assertRaises(ValueError):
                sync_projects.sync(config, output, lambda _: self.fail("must not fetch"))
            self.assertFalse(output.exists())

    def test_missing_cache_does_not_block_display_on_outage(self):
        with tempfile.TemporaryDirectory() as folder:
            config, output = Path(folder) / "projects.toml", Path(folder) / "cache.json"
            config.write_text('[[items]]\nrepo="owner/first"\n')
            def fail(_):
                raise TimeoutError()
            self.assertEqual(sync_projects.sync(config, output, fail), {})
            self.assertEqual(json.loads(output.read_text()), {})


if __name__ == "__main__":
    unittest.main()
