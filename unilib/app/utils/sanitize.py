"""
HTML sanitization utility using bleach.
Strips dangerous tags/attributes from Quill editor output before saving to DB.
"""
import bleach

# Tags yang diizinkan dari Quill editor
ALLOWED_TAGS = [
    'p', 'br', 'b', 'i', 'u', 'strong', 'em', 's',
    'ul', 'ol', 'li',
    'h2', 'h3', 'h4',
    'a', 'blockquote', 'pre', 'code', 'span',
]

# Atribut yang diizinkan per tag
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'target', 'rel'],
    'span': ['class'],
}


def clean_html(value: str | None) -> str:
    """Sanitize HTML from rich text editor. Returns empty string if None."""
    if not value:
        return ''
    return bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )
