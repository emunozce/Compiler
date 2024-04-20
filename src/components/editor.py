"""This module contains the Editor class that will be used to write the code"""

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qsci import QsciScintilla, QsciLexerCustom


class Editor(QsciScintilla):
    """This class is the editor widget that will be used to write the code"""

    cursorPositionChangedSignal = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

        self.cursorPositionChanged.connect(self.handle_cursor_position_changed)

        # Encoding
        self.setUtf8(True)

        # Set the font
        self.window_font = QFont("Monospace", 12)  # Set the font of the window
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
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setCaretLineBackgroundColor(QColor("#1A0089FF"))

        # EOL
        self.setEolMode(QsciScintilla.EolUnix)
        self.setEolVisibility(False)

        # Lexer

        self.setLexer()

        # Line Numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)

    def handle_cursor_position_changed(self, line, index):
        """This method is called every time the cursor position changes"""
        self.cursorPositionChangedSignal.emit(line, index)

    def handle_text_changed(self):
        """This method is called every time the content of the editor changes"""
        line, index = self.getCursorPosition()
        self.cursorPositionChangedSignal.emit(line, index)
