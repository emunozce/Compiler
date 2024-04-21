"""This module contains the Editor class that will be used to write the code"""

import builtins
import keyword
import pkgutil
import types
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qsci import QsciScintilla, QsciLexerCustom, QsciAPIs


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

        self.pylexer = CustomLexer(self)
        self.pylexer.setDefaultFont(self.window_font)

        self.setLexer(self.pylexer)

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


class CustomLexer(QsciLexerCustom):
    """This class is a custom"""

    def __init__(self, parent):
        super(CustomLexer, self).__init__(parent)

        self.color1 = "#abb2bf"
        self.color2 = "#282c34"

        # Default Settings
        self.setDefaultColor(QColor(self.color1))
        self.setDefaultPaper(QColor(self.color2))
        self.setDefaultFont(QFont("Monospace", 12))

        # Keywords
        self.KEYWORD_LIST = keyword.kwlist

        self.builtin_functions_names = [
            name
            for name, obj in vars(builtins).items()
            if isinstance(obj, types.BuiltinFunctionType)
        ]

        # Color per Style
        self.DEFAULT = 0
        self.NUMBER = 1
        self.IDENTIFIER = 2
        self.KEYWORD = 3
        self.COMMENT = 4
        self.ARITHMETIC_OPERATOR = 5
        self.RELATIONAL_OPERATOR = 6

        # Styles
        self.setColor(QColor(self.color1), self.DEFAULT)
        self.setColor(QColor("#d19a66"), self.NUMBER)
        self.setColor(QColor("#61afef"), self.IDENTIFIER)
        self.setColor(QColor("#e06c75"), self.KEYWORD)
        self.setColor(QColor("#5c6370"), self.COMMENT)
        self.setColor(QColor("#98c379"), self.ARITHMETIC_OPERATOR)
        self.setColor(QColor("#61afef"), self.RELATIONAL_OPERATOR)

        # Paper Color
        self.setPaper(QColor(self.color2), self.DEFAULT)
        self.setPaper(QColor(self.color2), self.NUMBER)
        self.setPaper(QColor(self.color2), self.IDENTIFIER)
        self.setPaper(QColor(self.color2), self.KEYWORD)
        self.setPaper(QColor(self.color2), self.COMMENT)
        self.setPaper(QColor(self.color2), self.ARITHMETIC_OPERATOR)
        self.setPaper(QColor(self.color2), self.RELATIONAL_OPERATOR)

        # Font
        self.setFont(QFont("Monospace", 12), self.DEFAULT)
        self.setFont(QFont("Monospace", 12), self.NUMBER)
        self.setFont(QFont("Monospace", 12), self.IDENTIFIER)
        self.setFont(QFont("Monospace", 12), self.KEYWORD)
        self.setFont(QFont("Monospace", 12), self.COMMENT)
        self.setFont(QFont("Monospace", 12), self.ARITHMETIC_OPERATOR)
        self.setFont(QFont("Monospace", 12), self.RELATIONAL_OPERATOR)

    def language(self):
        return "CustomLexer"

    def description(self, style):
        if style == self.DEFAULT:
            return "Default"
        elif style == self.NUMBER:
            return "Number"
        elif style == self.IDENTIFIER:
            return "Identifier"
        elif style == self.KEYWORD:
            return "Keyword"
        elif style == self.COMMENT:
            return "Comment"
        elif style == self.ARITHMETIC_OPERATOR:
            return "Arithmetic Operator"
        elif style == self.RELATIONAL_OPERATOR:
            return "Relational Operator"
        else:
            return ""

    def styleText(self, start, end):
        # Called everytime the editors text has changed
        self.startStyling(start)
        editor: QsciScintilla = self.parent()

        text = editor.text()[start:end]
