from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFrame,
    QHBoxLayout,
    QSizePolicy,
    QSplitter,
    QFileSystemModel,
    QTreeView,
    QVBoxLayout,
    QTabWidget,
    QLabel,
    QFileDialog,
    QWidget,
    QStatusBar,
)
from PyQt5.QtCore import Qt, QDir, QSize, QModelIndex
from PyQt5.QtGui import QFont, QPixmap, QColor

from PyQt5.Qsci import QsciScintilla, QsciScintillaBase


class Editor(QsciScintilla):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

        # Encoding
        self.setUtf8(True)

        # Set the font
        self.window_font = QFont("Droid Sans Mono", 12)  # Set the font of the window
        self.setFont(self.window_font)  # Set the font of the window

        # Set the font of the self
        self.setFont(self.window_font)

        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # identation
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # caret
        self.setCaretForegroundColor(QColor("#dedcdc"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setCallTipsBackgroundColor(QColor("#2c313c"))

        # EOL
        self.setEolMode(QsciScintilla.EolUnix)
        self.setEolVisibility(False)

        # Line Numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)
