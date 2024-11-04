#!/usr/bin/env python3
"""Module for testing GithubOrgClient functions."""
import unittest
from typing import Dict, Any
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, expected: Dict[str, Any], mock_get_json: MagicMock) -> None:
        """Test that GithubOrgClient.org returns the correct data."""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org)
        self.assertEqual(client.org(), expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self) -> None:
        """Tests that _public_repos_url property returns correct URL."""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': "https://api.github.com/users/google/repos"}
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests that public_repos method returns expected list of repos."""
        mock_get_json.return_value = [
            {"name": "episodes.dart", "private": False},
            {"name": "kratu", "private": False}
        ]
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/users/google/repos"
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                ["episodes.dart", "kratu"]
            )
            mock_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict[str, Any], key: str, expected: bool) -> None:
        """Tests that has_license method accurately checks for a license."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, key), expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class-wide fixtures."""
        route_payloads = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def side_effect(url):
            return Mock(**{'json.return_value': route_payloads[url]}) if url in route_payloads else HTTPError

        cls.get_patcher = patch("requests.get", side_effect=side_effect)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests public_repos method with expected repository data."""
        self.assertEqual(GithubOrgClient("google").public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Tests public_repos method for repositories with a specific license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes class-wide fixtures."""
        cls.get_patcher.stop()
