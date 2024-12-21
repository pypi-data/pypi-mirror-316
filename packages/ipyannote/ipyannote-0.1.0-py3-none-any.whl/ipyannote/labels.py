from typing import Optional
from ipywidgets import jslink
import anywidget
import traitlets

import importlib.metadata
import pathlib


try:
    __version__ = importlib.metadata.version("ipyannote")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

class Labels(anywidget.AnyWidget):

    _esm = pathlib.Path(__file__).parent / "static" / "labels.js"
    _css = pathlib.Path(__file__).parent / "static" / "labels.css"

    labels = traitlets.Dict().tag(sync=True)
    color_cycle = traitlets.Int(0).tag(sync=True)

    def __init__(self, labels: Optional[dict[str, str]] = None):
        super().__init__()
        if labels:
            self.labels = labels

    def sync(self, waveform: "Labels | Waveform"): # type: ignore
        keys = ["labels", "color_cycle"]
        unlinks = {key: jslink((self, key), (waveform, key)).unlink for key in keys}

        def unlink():
            for unlink in unlinks.values():
                unlink()

        return unlink