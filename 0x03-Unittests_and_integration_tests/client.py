#!/usr/bin/env python3
"""Client to interact with Github organizations
"""
from typing import List, Dict
from utils import get_json, access_nested_map, memoize


class GithubOrgClient:
    """Github organization client class
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize with the organization's name"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Memoized organization data"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """URL to access public repositories"""
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """Memoized repository payload data"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """List of public repository names, optionally filtered by license"""
        payload = self.repos_payload
        repos = [
            repo["name"] for repo in payload
            if license is None or self.has_license(repo, license)
        ]
        return repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Determine if repository has specified license"""
        assert license_key is not None, "license_key cannot be None"
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
