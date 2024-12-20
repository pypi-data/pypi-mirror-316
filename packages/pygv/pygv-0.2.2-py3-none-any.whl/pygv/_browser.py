from __future__ import annotations

import pathlib

import anywidget
import msgspec
import traitlets

from ._config import Config


class Browser(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    config = traitlets.Instance(Config).tag(
        sync=True, to_json=lambda x, _: msgspec.to_builtins(x)
    )

    def __init__(self, config: Config) -> None:
        super().__init__(config=config.servable())
