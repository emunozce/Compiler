"""This module contains the Editor class that will be used to write the code"""

import builtins
import re
import types
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
        self.setMatchedBraceBackgroundColor(QColor("#CF571B04"))

        # identation
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # caret
        self.setCaretLineVisible(True)
        self.setCaretWidth(1)
        self.setCaretForegroundColor(QColor("#ffffff"))
        self.setCaretLineBackgroundColor(QColor("#3A0089FF"))

        # EOL
        self.setEolMode(QsciScintilla.EolUnix)
        self.setEolVisibility(False)

        # Lexer
        self.setLexer(CustomLexer(self))

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
    """This class is a custom lexer that will be used **ONLY** to highlight the code in the editor."""

    def __init__(self, parent):
        super(CustomLexer, self).__init__(parent)

        self.color1 = "#abb2bf"
        self.color2 = "#282c34"

        # Default Settings
        self.setDefaultColor(QColor(self.color1))
        self.setDefaultPaper(QColor(self.color2))
        self.setDefaultFont(QFont("Monospace", 12))

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
        self.setColor(QColor("#fcdf03"), self.NUMBER)
        self.setColor(QColor("#09eded"), self.IDENTIFIER)
        self.setColor(QColor("#fa37b9"), self.KEYWORD)
        self.setColor(QColor("#6ff781"), self.COMMENT)
        self.setColor(QColor("#de0000"), self.ARITHMETIC_OPERATOR)
        self.setColor(QColor("#1685f5"), self.RELATIONAL_OPERATOR)

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
        ############################## Patterns ##############################
        identifier_pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        reserved_words_pattern = re.compile(
            r"\b(if|else|do|while|switch|case|double|main|cin|cout|int|real|then|end|until)\b"
        )
        number_pattern = re.compile(r"\b\d+\b")
        aritmethic_op_pattern = re.compile(r"\+|-|\*|/|%|\^")
        relational_op_pattern = re.compile(r"<|>|!|=")
        p = re.compile(r"//.*?$|/\*|\*/|\b\w+\b|\W", re.MULTILINE)
        ######################################################################

        # Called everytime the editors text has changed
        self.startStyling(start)
        editor: QsciScintilla = self.parent()

        text = editor.text()[start:end]

        token_list = [
            (token, len(bytearray(token, "utf-8"))) for token in p.findall(text)
        ]

        is_multiline_comment = False

        if start > 0:
            previous_style_nr = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style_nr == self.COMMENT:
                is_multiline_comment = True

        for token in token_list:
            if is_multiline_comment:
                self.setStyling(token[1], self.COMMENT)
                if token[0] == "*/":
                    is_multiline_comment = False
            elif token[0].startswith("//"):
                self.setStyling(token[1], self.COMMENT)
            elif reserved_words_pattern.match(token[0]):
                self.setStyling(token[1], self.KEYWORD)
            elif identifier_pattern.match(token[0]):
                self.setStyling(token[1], self.IDENTIFIER)
            elif number_pattern.match(token[0]) or token[0] == ".":
                self.setStyling(token[1], self.NUMBER)
            elif token[0] == "/*":
                is_multiline_comment = True
                self.setStyling(token[1], self.COMMENT)
            elif aritmethic_op_pattern.match(token[0]):
                self.setStyling(token[1], self.ARITHMETIC_OPERATOR)
            elif relational_op_pattern.match(token[0]):
                self.setStyling(token[1], self.RELATIONAL_OPERATOR)
            else:
                self.setStyling(token[1], self.DEFAULT)
