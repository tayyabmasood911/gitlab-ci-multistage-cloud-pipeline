import os
import unittest
import yaml

class TestGitLabCIPipeline(unittest.TestCase):
    def setUp(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.ci_file = os.path.join(self.root, ".gitlab-ci.yml")

    def test_core_files_exist(self):
        required = [
            "README.md",
            "Makefile",
            "SECURITY.md",
            ".gitattributes",
            ".gitlab-ci.yml",
            "templates/security-scans.gitlab-ci.yml",
            "k8s/staging/deployment.yaml",
            "k8s/production/deployment.yaml",
            "scripts/lint_gitlab_ci.py",
            "scripts/healthcheck.sh",
            "docs/architecture.svg"
        ]
        for f in required:
            p = os.path.join(self.root, f)
            self.assertTrue(os.path.exists(p), f"Required file '{f}' must exist")

    def test_pipeline_stages(self):
        with open(self.ci_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        stages = data.get("stages", [])
        expected = ["validate", "test", "security", "build", "deploy-staging", "deploy-production"]
        for s in expected:
            self.assertIn(s, stages)

    def test_caching_and_dind(self):
        with open(self.ci_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.assertIn("cache", data)
        self.assertIn("docker_dind_build", data)
        self.assertEqual(data["deploy_to_production"].get("when"), "manual")

    def test_gitattributes_content(self):
        path = os.path.join(self.root, ".gitattributes")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("* text=auto eol=lf", content)
        self.assertIn("Makefile linguist-vendored=true", content)

if __name__ == "__main__":
    unittest.main()
