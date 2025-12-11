"""
SIMBA Backend - Validation Utilities

Input validation helpers.
"""

import re
from typing import List
from app.config import settings
from app.utils.exceptions import ValidationError


def validate_file_extension(filename: str) -> bool:
    """Validate file extension"""
    ext = filename.split(".")[-1].lower()
    return ext in settings.ALLOWED_EXTENSIONS


def validate_file_size(size_bytes: int) -> bool:
    """Validate file size"""
    return size_bytes <= settings.max_upload_size_bytes


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_uuid(uuid_str: str) -> bool:
    """Validate UUID format"""
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_str))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename"""
    # Remove path separators
    filename = filename.replace("/", "_").replace("\\", "_")

    # Remove special characters except dots, hyphens, underscores
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)

    return filename


def validate_tool_parameters(parameters: dict, schema: dict) -> None:
    """Validate tool parameters against schema"""
    required = schema.get("required", [])

    # Check required parameters
    for param in required:
        if param not in parameters:
            raise ValidationError(
                f"Missing required parameter: {param}",
                details={"required": required, "provided": list(parameters.keys())}
            )

    # Validate types (basic)
    properties = schema.get("properties", {})
    for param, value in parameters.items():
        if param in properties:
            expected_type = properties[param].get("type")
            if expected_type == "string" and not isinstance(value, str):
                raise ValidationError(f"Parameter {param} must be a string")
            elif expected_type == "number" and not isinstance(value, (int, float)):
                raise ValidationError(f"Parameter {param} must be a number")
            elif expected_type == "boolean" and not isinstance(value, bool):
                raise ValidationError(f"Parameter {param} must be a boolean")
            elif expected_type == "array" and not isinstance(value, list):
                raise ValidationError(f"Parameter {param} must be an array")
            elif expected_type == "object" and not isinstance(value, dict):
                raise ValidationError(f"Parameter {param} must be an object")


def validate_message_content(content: str, max_length: int = 50000) -> None:
    """Validate message content"""
    if not content or not content.strip():
        raise ValidationError("Message content cannot be empty")

    if len(content) > max_length:
        raise ValidationError(
            f"Message content exceeds maximum length of {max_length} characters"
        )
