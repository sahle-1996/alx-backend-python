#!/usr/bin/env python3
"""Tests with parameterization and patching for GithubOrgClient."""
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """Class for testing GithubOrgClient methods."""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test if GithubOrgClient.org returns correct data."""
        client = GithubOrgClient(org_name)
        client.org()
        mock_get_json.assert_called_once_with(client.ORG_URL.format(org=org_name))

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url for correct URL."""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "example_url"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "example_url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test if public_repos returns the correct list of repos."""
        repos = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = repos
        with patch("client.GithubOrgClient._public_repos_url", return_value="mock_url"):
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once()
    
    @parameterized.expand([
        ({"license": {"key": "valid_license"}}, "valid_license", True),
        ({"license": {"key": "different_license"}}, "valid_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test if has_license correctly identifies a repo's license."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up mock responses for integration tests."""
        responses = {"return_value.json.side_effect": [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload
        ]}
        cls.get_patcher = patch("requests.get", **responses)
        cls.mock_get = cls.get_patcher.start()

    def test_public_repo(self):
        """Integration test for public_repos with expected output."""
        client = GithubOrgClient("Google")
        self.assertEqual(client.org, self.org_payload)
        self.assertEqual(client.repos_payload, self.repos_payload)
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("nonexistent_license"), [])
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """Test public_repos with a specific license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("nonexistent_license"), [])
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
        self.mock_get.assert_called()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all integration tests have run."""
        cls.get_patcher.stop()
