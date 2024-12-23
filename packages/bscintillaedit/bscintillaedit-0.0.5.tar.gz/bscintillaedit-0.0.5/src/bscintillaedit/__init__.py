"""PySide6 bindings for the `BScintillaEdit` widget derived from
[QScrollArea](https://doc.qt.io/qt-6/qscrollarea.html) that wraps a
`ScintillaEditBase` widget from [Scintilla](https://www.scintilla.org/).
"""

# the binding will not load if we don't explicitly importing PySide6.QtWidgets
import PySide6.QtWidgets

# import the C++ classes wrapped by the binding
from .bscintillaedit import (
    BScintillaEdit,
)

# make the C++ classes wrapped by binding available directly from the python
# package
__all__ = [
    "BScintillaEdit",
]

__version__ = "0.0.5"
