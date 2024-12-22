# BScintillaEdit

The `BScintillaEdit` is a simple text edit control derived from a `QScrollArea` that embeds a `ScintillaBaseEdit` from [Scintilla](https://www.scintilla.org/).

The Python bindings are made with [shiboken](https://doc.qt.io/qtforpython-6/shiboken6/index.html).

## PyPI

The package can be installed from [PyPI](https://pypi.org/project/bscintillaedit/):

```bash
pip install bscintillaedit
```

## Usage

```python
from PySide6.QtWidgets import QApplication

from bscintillaedit import BScintillaEdit

SAMPLE_TEXT = """
Lorem ipsum odor amet, consectetuer adipiscing elit.

Dui enim odio natoque libero accumsan mus maecenas himenaeos.

Sapien est turpis maecenas diam turpis ultrices tempus.
"""


def run() -> None:
    """Start application."""
    app = QApplication()
    window = BScintillaEdit()
    window.setLineEndVisible(True)
    window.setLineNumbersVisible(True)
    window.setLineWrapped(True)
    window.setText(SAMPLE_TEXT)
    window.resize(300, 300)
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
```

![sample_app](https://gitlab.com/iborco-pyside/bscintillaedit/-/raw/master/docs/python_sample.png?ref_type=heads)

## License

This project uses:

* the code from the [Scintilla](https://www.scintilla.org/) project as a submodule installed in `src/core_lib/scintilla`
  * all the code under `src/core_lib/scintilla` is covered by the [scintilla license](https://www.scintilla.org/License.txt), a [Historical Permission Notice and Disclaimer](https://en.wikipedia.org/wiki/Historical_Permission_Notice_and_Disclaimer) type of license
* the extra [Qt 5 Compatibility Module](https://doc.qt.io/qt-6/qtcore5-index.html)
  * because the [PySide6](https://pypi.org/project/PySide6/) package doesn't include this module, the `Qt6Core5Compat` shared library is deployed within the *wheel*
  * the *Qt 5 Compatibility Module* is available under these [licenses](https://doc.qt.io/qt-6/qtcore5-index.html#licenses-and-attributions):
    * commercial licenses from [The Qt Company](http://www.qt.io/about-us/),
    * the [GNU Lesser General Public License, version 3](http://www.gnu.org/licenses/lgpl-3.0.html), or
    * the [GNU General Public License, version 2](http://www.gnu.org/licenses/gpl-2.0.html)

All the other code from this project is licensed under the [MIT License](https://gitlab.com/iborco-pyside/bscintillaedit/-/blob/master/LICENSE.md).

This software is <ins>**not related**</ins> to the [QScintilla](https://www.riverbankcomputing.com/software/qscintilla/) or [PyQt](https://www.riverbankcomputing.com/software/pyqt/) projects.
