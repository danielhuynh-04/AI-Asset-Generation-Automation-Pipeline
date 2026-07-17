"""
validator.py — Input validation module
Kiểm tra từng row từ Google Sheets trước khi đưa vào pipeline.
Áp dụng tư duy data leakage control: validate tại nguồn, không để lỗi lan xuống downstream.
"""
import re
from dataclasses import dataclass
from typing import Optional


VALID_FORMATS = {"PNG", "JPG", "GIF", "MP3"}
VALID_MODELS  = {"Gemini", "Pollinations"}


@dataclass
class ValidationResult:
    is_valid: bool
    error: Optional[str] = None
    normalized: Optional[dict] = None  # row sau khi chuẩn hóa


def _is_valid_url(url: str) -> bool:
    """Kiểm tra URL format cơ bản."""
    pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def validate_row(row: dict) -> ValidationResult:
    """
    Validate một row từ Google Sheet.
    
    Args:
        row: dict với keys: id, description, example_url, output_format, model
    
    Returns:
        ValidationResult(is_valid, error, normalized)
    
    Ví dụ test cases:
        - description là null     → FAILED với error "description is required"
        - output_format = "WEBP"  → FAILED với error "Invalid output_format"
        - model = "GPT4"          → FAILED với error "Invalid model"
        - example_url sai format  → WARNING (không fail, chỉ log)
        - Tất cả hợp lệ          → SUCCESS
    """
    errors = []

    # --- Kiểm tra description ---
    description = str(row.get("description", "")).strip()
    if not description or description.lower() in ("none", "null", ""):
        errors.append("description is required and cannot be empty")
    elif len(description) < 10:
        errors.append(f"description too short ({len(description)} chars, min 10)")

    # --- Kiểm tra output_format ---
    output_format = str(row.get("output_format", "")).strip().upper()
    if output_format not in VALID_FORMATS:
        errors.append(f"Invalid output_format '{output_format}'. Must be one of: {VALID_FORMATS}")

    # --- Kiểm tra model ---
    model = str(row.get("model", "")).strip()
    # Normalize: case-insensitive check
    model_normalized = None
    for valid in VALID_MODELS:
        if model.lower() == valid.lower():
            model_normalized = valid
            break
    if not model_normalized:
        errors.append(f"Invalid model '{model}'. Must be one of: {VALID_MODELS}")

    # --- Validate example_url (optional, chỉ warn) ---
    example_url = str(row.get("example_url", "")).strip()
    url_warning = None
    if example_url and example_url.lower() not in ("none", "null", ""):
        if not _is_valid_url(example_url):
            url_warning = f"example_url '{example_url[:50]}' may be invalid — proceeding anyway"
    else:
        example_url = None

    if errors:
        return ValidationResult(is_valid=False, error=" | ".join(errors))

    normalized = {
        "description": description,
        "output_format": output_format,
        "model": model_normalized,
        "example_url": example_url,
        "url_warning": url_warning,
    }
    return ValidationResult(is_valid=True, normalized=normalized)
