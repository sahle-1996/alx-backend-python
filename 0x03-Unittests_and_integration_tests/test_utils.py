#!/usr/bin/env python3
"""Client for accessing GitHub organization information"""

from typing import List, Dict
from utils import get_json, access_nested_map, memoize


class GithubOrgClient:
    """GitHub organization client for handling API requests"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize with organization name"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Retrieve and memoize organization data"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """URL for fetching public repositories"""
        return self.org.get("repos_url", "")

    @memoize
    def repos_payload(self) -> Dict:
        """Fetch and memoize repositories payload"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Retrieve public repositories with optional license filter"""
        repos_data = self.repos_payload
        return [
            repo["name"] for repo in repos_data
            if license is None or self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repository has a specified license"""
        assert license_key, "license_key must not be None"
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
