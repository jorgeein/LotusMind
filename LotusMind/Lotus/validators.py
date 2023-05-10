import os

from django.core.exceptions import ValidationError


def validate_svg(value):
    ext = os.path.splitext(value.name)[1]  # Get file extension
    if ext.lower() != '.svg':
        raise ValidationError('Only SVG files are allowed.')
