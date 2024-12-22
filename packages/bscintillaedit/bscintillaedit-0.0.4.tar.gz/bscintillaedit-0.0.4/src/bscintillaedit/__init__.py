"""Provides a `BScintillaEdit` text edit control based on
[QScrollArea](https://doc.qt.io/qt-6/qscrollarea.html) and embedding a
`ScintillaEditBase` from [Scintilla](https://www.scintilla.org/).
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

__version__ = "0.0.4"
