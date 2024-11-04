#!/usr/bin/env python3
"""A module for testing utilities."""
import unittest
from typing import Any, Dict, Tuple
from unittest.mock import patch, Mock
from parameterized import parameterized

from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class TestNestedMapAccess(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"x": 10}, ("x",), 10),
        ({"x": {"y": 5}}, ("x",), {"y": 5}),
        ({"x": {"y": 5}}, ("x", "y"), 5),
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict[str, Any],
            path: Tuple[str, ...],
            expected: Any
    ) -> None:
        """Ensures access_nested_map produces expected output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("x",), KeyError),
        ({"x": 10}, ("x", "y"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict[str, Any],
            path: Tuple[str, ...],
            exception: Exception
    ) -> None:
        """Checks if access_nested_map raises expected exceptions."""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestJsonFetch(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://test.com", {"key": "value"}),
        ("http://anotherurl.com", {"result": False}),
    ])
    def test_get_json(
            self,
            url: str,
            response_payload: Dict[str, Any]
    ) -> None:
        """Tests that get_json returns the correct JSON response."""
        mock_attributes = {'json.return_value': response_payload}
        with patch("requests.get", return_value=Mock(**mock_attributes)) as req_get:
            self.assertEqual(get_json(url), response_payload)
            req_get.assert_called_once_with(url)


class TestMemoization(unittest.TestCase):
    """Tests for the memoize function."""

    def test_memoize(self) -> None:
        """Tests memoize decorator caching behavior."""

        class SampleClass:
            def compute_value(self) -> int:
                return 99

            @memoize
            def cached_value(self) -> int:
                return self.compute_value()

        with patch.object(
                SampleClass,
                "compute_value",
                return_value=99
        ) as mock_method:
            instance = SampleClass()
            self.assertEqual(instance.cached_value(), 99)
            self.assertEqual(instance.cached_value(), 99)
            mock_method.assert_called_once()
