#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class"""
import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests methods in GithubOrgClient"""
    
    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, response: Dict, mock_get_json: MagicMock) -> None:
        """Tests the `org` method for correct return value"""
        mock_get_json.return_value = response
        gh_client = GithubOrgClient(org)
        self.assertEqual(gh_client.org(), response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self) -> None:
        """Tests `_public_repos_url` property"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': "https://api.github.com/users/google/repos"}
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests `public_repos` method"""
        repos_payload = [
            {"name": "episodes.dart"},
            {"name": "kratu"}
        ]
        mock_get_json.return_value = repos_payload
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/users/google/repos"
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                ["episodes.dart", "kratu"]
            )
            mock_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests `has_license` method"""
        gh_client = GithubOrgClient("test_org")
        self.assertEqual(gh_client.has_license(repo, key), expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class-level resources"""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload
        }

        def get_mock(url):
            return Mock(**{'json.return_value': route_payload.get(url, HTTPError)})

        cls.get_patcher = patch("requests.get", side_effect=get_mock)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests `public_repos` method"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self) -> None:
        """Tests `public_repos` with license filter"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleans up class-level resources"""
        cls.get_patcher.stop()
