#!/usr/bin/env python3
"""Module for testing utility functions."""
import unittest
from typing import Any, Dict, Tuple
from unittest.mock import patch, Mock
from parameterized import parameterized

from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict[str, Any],
            path: Tuple[str, ...],
            expected: Any
    ) -> None:
        """Checks output of access_nested_map."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict[str, Any],
            path: Tuple[str, ...],
            exception: Exception
    ) -> None:
        """Ensures access_nested_map raises KeyError when expected."""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
            self,
            url: str,
            mock_response: Dict[str, Any]
    ) -> None:
        """Validates get_json response."""
        mock_attrs = {'json.return_value': mock_response}
        with patch("requests.get", return_value=Mock(**mock_attrs)) as mock_get:
            self.assertEqual(get_json(url), mock_response)
            mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator function."""

    def test_memoize(self) -> None:
        """Tests that memoize caches results properly."""

        class DummyClass:
            def get_value(self) -> int:
                return 42

            @memoize
            def memoized_value(self) -> int:
                return self.get_value()

        with patch.object(
                DummyClass,
                "get_value",
                return_value=42
        ) as mock_method:
            instance = DummyClass()
            self.assertEqual(instance.memoized_value(), 42)
            self.assertEqual(instance.memoized_value(), 42)
            mock_method.assert_called_once()
