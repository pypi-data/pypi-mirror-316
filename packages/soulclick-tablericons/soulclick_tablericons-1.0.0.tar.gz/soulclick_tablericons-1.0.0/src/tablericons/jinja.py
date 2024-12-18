from __future__ import annotations

from markupsafe import Markup

import tablericons


def tablericon_outline(name: str, *, size: int | None = 24, **kwargs: object) -> str:
    return _render_icon("outline", name, size, **kwargs)


def tablericon_filled(name: str, *, size: int | None = 24, **kwargs: object) -> str:
    return _render_icon("filled", name, size, **kwargs)


def _render_icon(style: str, name: str, size: int | None, **kwargs: object) -> str:
    return Markup(tablericons._render_icon(style, name, size, **kwargs))
