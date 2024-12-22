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
