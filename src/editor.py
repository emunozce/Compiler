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
from PyQt5.QtCore import Qt, QDir, QSize, QModelIndex,pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QColor


from PyQt5.Qsci import QsciScintilla, QsciScintillaBase


class Editor(QsciScintilla):
    cursorPositionChangedSignal = pyqtSignal(int, int)

    def __init__(self):
        super(Editor, self).__init__()

        self.cursorPositionChanged.connect(self.handleCursorPositionChanged)

        self.modified = False

        # Conectar el evento de modificación del documento
        self.textChanged.connect(self.handle_text_changed)
        

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
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)

        # EOL
        self.setEolMode(QsciScintilla.EolUnix)
        self.setEolVisibility(False)

        # Line Numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)

    def handleCursorPositionChanged(self, line, index):
        # Emitir la señal personalizada con la información de la posición del cursor
        self.cursorPositionChangedSignal.emit(line, index)

    def handle_text_changed(self):
        # Este método se llama cada vez que el contenido del editor cambia
        self.modified = True
        line, index = self.getCursorPosition()
        self.cursorPositionChangedSignal.emit(line, index)

    
