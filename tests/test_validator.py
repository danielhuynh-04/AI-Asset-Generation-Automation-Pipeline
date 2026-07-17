"""
test_validator.py — Unit tests for validator module
Áp dụng tư duy sanity check / permutation test từ ML pipeline.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from validator import validate_row, ValidationResult


# ─── Happy path ───────────────────────────────────────────────────────────────
def test_valid_row_returns_success():
    row = {
        "description": "A glossy blue bingo ball with white shine, transparent background",
        "example_url": "https://example.com/ball.png",
        "output_format": "PNG",
        "model": "Gemini",
    }
    result = validate_row(row)
    assert result.is_valid is True
    assert result.error is None
    assert result.normalized["output_format"] == "PNG"
    assert result.normalized["model"] == "Gemini"


def test_valid_row_mp3():
    row = {
        "description": "Celebratory winning sound effect with upbeat tone",
        "example_url": "",
        "output_format": "MP3",
        "model": "Pollinations",
    }
    result = validate_row(row)
    assert result.is_valid is True


# ─── Description validation ───────────────────────────────────────────────────
def test_empty_description_fails():
    row = {"description": "", "output_format": "PNG", "model": "Gemini"}
    result = validate_row(row)
    assert result.is_valid is False
    assert "description is required" in result.error


def test_null_description_fails():
    row = {"description": "null", "output_format": "PNG", "model": "Gemini"}
    result = validate_row(row)
    assert result.is_valid is False


def test_short_description_fails():
    row = {"description": "hi", "output_format": "PNG", "model": "Gemini"}
    result = validate_row(row)
    assert result.is_valid is False
    assert "too short" in result.error


# ─── Output format validation ─────────────────────────────────────────────────
def test_invalid_output_format_fails():
    row = {
        "description": "A detailed game character with cartoon style",
        "output_format": "WEBP",  # Invalid
        "model": "Gemini",
    }
    result = validate_row(row)
    assert result.is_valid is False
    assert "output_format" in result.error


def test_case_insensitive_format():
    """PNG, png, Png đều hợp lệ — normalized thành uppercase"""
    row = {
        "description": "A glossy bingo frame with gold border",
        "output_format": "png",  # lowercase
        "model": "Gemini",
    }
    result = validate_row(row)
    assert result.is_valid is True
    assert result.normalized["output_format"] == "PNG"


# ─── Model validation ─────────────────────────────────────────────────────────
def test_invalid_model_fails():
    row = {
        "description": "A game background with theatrical lighting",
        "output_format": "PNG",
        "model": "GPT4",  # Invalid
    }
    result = validate_row(row)
    assert result.is_valid is False
    assert "model" in result.error


def test_pollinations_model_valid():
    row = {
        "description": "A reward card with golden frame and star decoration",
        "output_format": "JPG",
        "model": "pollinations",  # case-insensitive
    }
    result = validate_row(row)
    assert result.is_valid is True
    assert result.normalized["model"] == "Pollinations"


# ─── URL validation (warning, not fail) ──────────────────────────────────────
def test_invalid_url_does_not_fail():
    """Sai URL format chỉ là warning — pipeline vẫn tiếp tục"""
    row = {
        "description": "A bingo ball with glossy blue surface",
        "example_url": "not_a_valid_url",
        "output_format": "PNG",
        "model": "Gemini",
    }
    result = validate_row(row)
    assert result.is_valid is True  # Không fail
    assert result.normalized["url_warning"] is not None


def test_missing_url_is_ok():
    row = {
        "description": "A bingo ball with glossy green surface",
        "output_format": "PNG",
        "model": "Gemini",
    }
    result = validate_row(row)
    assert result.is_valid is True
    assert result.normalized["example_url"] is None
