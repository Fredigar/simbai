"""
SIMBA Backend - Helper Functions

General purpose utility functions.
"""

import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict


def generate_uuid() -> str:
    """Generate a new UUID"""
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """Generate a short random ID"""
    return uuid.uuid4().hex[:length]


def hash_string(text: str) -> str:
    """Hash a string using SHA-256"""
    return hashlib.sha256(text.encode()).hexdigest()


def get_current_timestamp() -> datetime:
    """Get current UTC timestamp"""
    return datetime.utcnow()


def format_timestamp(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime as string"""
    return dt.strftime(fmt)


def parse_timestamp(timestamp_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse timestamp string to datetime"""
    return datetime.strptime(timestamp_str, fmt)


def get_relative_time(dt: datetime) -> str:
    """Get relative time string (e.g., '2 hours ago')"""
    now = datetime.utcnow()
    diff = now - dt

    if diff.total_seconds() < 60:
        return "just now"
    elif diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.days < 7:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.days < 30:
        weeks = diff.days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    else:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Chunk text into overlapping segments"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at sentence boundary
        if end < len(text):
            last_period = chunk.rfind(". ")
            if last_period > chunk_size * 0.5:  # Don't break too early
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def dict_to_flat(nested_dict: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dictionary"""
    items = []

    for k, v in nested_dict.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            items.extend(dict_to_flat(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


def remove_none_values(d: Dict[str, Any]) -> Dict[str, Any]:
    """Remove keys with None values from dictionary"""
    return {k: v for k, v in d.items() if v is not None}


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def extract_mentions(text: str) -> list[str]:
    """Extract @mentions from text"""
    import re
    pattern = r'@(\w+)'
    return re.findall(pattern, text)


def calculate_file_hash(file_bytes: bytes) -> str:
    """Calculate hash of file content"""
    return hashlib.sha256(file_bytes).hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable form"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def parse_duration_ms(duration: timedelta) -> float:
    """Convert timedelta to milliseconds"""
    return duration.total_seconds() * 1000
