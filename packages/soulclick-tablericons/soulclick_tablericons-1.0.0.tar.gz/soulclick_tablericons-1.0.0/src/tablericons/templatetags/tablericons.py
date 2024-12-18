from __future__ import annotations

from django import template
from django.utils.safestring import SafeString
from django.utils.safestring import mark_safe

import tablericons

register = template.Library()


@register.simple_tag
def tablericon_outline(name: str, *, size: int | None = 24, **kwargs: object) -> str:
    return _render_icon("outline", name, size, **kwargs)


@register.simple_tag
def tablericon_filled(name: str, *, size: int | None = 24, **kwargs: object) -> str:
    return _render_icon("filled", name, size, **kwargs)


def _render_icon(style: str, name: str, size: int | None, **kwargs: object) -> str:
    # simple_tag's parsing loads passed strings as safe, but they aren't
    # Cast the SafeString's back to normal strings the only way possible, by
    # concatenating the empty string.
    fixed_kwargs = {
        key: (value + "" if isinstance(value, SafeString) else value)
        for key, value in kwargs.items()
    }
    return mark_safe(tablericons._render_icon(style, name, size, **fixed_kwargs))
