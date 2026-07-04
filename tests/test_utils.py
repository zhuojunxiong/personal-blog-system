"""Unit tests for utility functions in services.py."""
import pytest
from app.services import make_slug, normalize_text, parse_int_list, utcnow
from datetime import datetime, timezone


class TestMakeSlug:
    """Tests for make_slug()."""

    def test_basic_english(self):
        slug = make_slug("Hello World Flask")
        assert "Hello" in slug
        assert "World" in slug
        assert "Flask" in slug

    def test_chinese_text(self):
        slug = make_slug("Flask 入门指南")
        assert "Flask" in slug
        # Chinese characters should be preserved
        assert any("一" <= c <= "鿿" for c in slug)

    def test_special_characters(self):
        slug = make_slug("Hello!!! World???")
        # Special chars should be replaced with hyphens
        assert "Hello" in slug
        assert "World" in slug

    def test_empty_string(self):
        slug = make_slug("")
        assert len(slug) > 0  # Should generate UUID fallback

    def test_whitespace_only(self):
        slug = make_slug("   ")
        assert len(slug) > 0  # Should generate UUID fallback

    def test_max_length(self):
        long_text = "a" * 200
        slug = make_slug(long_text)
        assert len(slug) <= 120

    def test_leading_trailing_hyphens_removed(self):
        slug = make_slug("---hello---")
        assert not slug.startswith("-")
        assert not slug.endswith("-")

    def test_multiple_delimiters(self):
        slug = make_slug("hello...world!!!test")
        assert "hello" in slug
        assert "world" in slug
        assert "test" in slug


class TestNormalizeText:
    """Tests for normalize_text()."""

    def test_basic(self):
        assert normalize_text("  hello  ") == "hello"

    def test_none(self):
        assert normalize_text(None) == ""

    def test_empty_string(self):
        assert normalize_text("") == ""

    def test_whitespace_only(self):
        assert normalize_text("   \t\n  ") == ""

    def test_chinese(self):
        assert normalize_text("  你好世界  ") == "你好世界"


class TestParseIntList:
    """Tests for parse_int_list()."""

    def test_valid_list(self):
        result = parse_int_list(["1", "2", "3"])
        assert result == [1, 2, 3]

    def test_mixed_values(self):
        result = parse_int_list(["1", "abc", "3", "", None])
        assert result == [1, 3]

    def test_empty_list(self):
        result = parse_int_list([])
        assert result == []

    def test_all_invalid(self):
        result = parse_int_list(["a", "b", "c"])
        assert result == []

    def test_string_numbers(self):
        result = parse_int_list(["10", "20"])
        assert result == [10, 20]


class TestUtcNow:
    """Tests for utcnow()."""

    def test_returns_datetime(self):
        result = utcnow()
        assert isinstance(result, datetime)

    def test_is_naive(self):
        result = utcnow()
        assert result.tzinfo is None

    def test_is_recent(self):
        result = utcnow()
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        diff = abs((now - result).total_seconds())
        assert diff < 5  # Should be within 5 seconds
