import sys
import os
from pathlib import Path

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
)
from PyQt5.QtCore import Qt, QDir, QSize, QModelIndex
from PyQt5.QtGui import QFont, QPixmap

from PyQt5.Qsci import QsciScintilla


from editor import Editor
from menu import set_up_menu
from dock_panels import set_up_dock_panels, set_lexical_analysis_result
from lexer import get_lexycal_analysis


class MainWindow(QMainWindow):
    def __init__(self):  # Constructor
        super(QMainWindow, self).__init__()  # Call the constructor of the parent class
        self.init_ui()  # Call the method to initialize the UI

        self.current_file = None

    def init_ui(self):  # Method to initialize the UI
        self.setWindowTitle("IDE")  # Set the title of the window
        self.resize(1100, 900)  # Set the size of the window

        self.window_font = QFont("Droid Sans Mono", 12)  # Set the font of the window
        self.setFont(self.window_font)  # Set the font of the window

        set_up_menu(self)

        self.set_up_body()

        set_up_dock_panels(self)

        self.show()

    def get_editor(self) -> QsciScintilla:
        editor = Editor()
        return editor

    def is_binary(
        self, path: Path
    ) -> bool:  # Check if a file is binary (e.g. image, video, etc.)
        with open(path, "rb") as file:
            return b"\0" in file.read(1024)  # Check for null bytes

    def set_new_tab(self, path: Path, is_new_file=False):
        editor = self.get_editor()

        if is_new_file:
            self.tab_view.addTab(editor, "Untitled")
            self.setWindowTitle("Untitled")
            self.statusBar().showMessage("New file created", 2000)
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return

        if not path.is_file():
            return
        if self.is_binary(path):
            self.statusBar().showMessage("Cannot open binary files", 2000)
            return

        # Check if the file is already open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return

        # Create new tab
        self.tab_view.addTab(editor, path.name)
        if not is_new_file:
            with open(path, "r", encoding="utf-8") as file:
                editor.setText(file.read())
        self.setWindowTitle(path.name)
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path}", 2000)

    def new_file(self):
        self.set_new_tab(None, is_new_file=True)

    def open_file(self):
        ops = QFileDialog.Options()  # Create a file dialog
        # ops |= QFileDialog.DontUseNativeDialog
        new_file, _ = QFileDialog.getOpenFileName(
            self, "Pick a file", "", "All Files (*)", options=ops
        )

        if new_file == "":
            self.statusBar().showMessage("Cancelled", 2000)
            return
        f = Path(new_file)
        self.set_new_tab(f)

    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()

        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text(), encoding="utf-8")
        self.statusBar().showMessage(f"Saved {self.current_file}", 2000)

    def save_as(self):
        editor = self.tab_view.currentWidget()
        if editor is None:
            return

        file_path = QFileDialog.getSaveFileName(self, "Save as", os.getcwd())[0]
        if file_path == "":
            self.statusBar().showMessage("Cancelled", 2000)
            return
        path = Path(file_path)
        path.write_text(editor.text(), encoding="utf-8")
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path}", 2000)
        self.current_file = path

    def open_folder(self):
        ops = QFileDialog.Options()  # Create a file dialog
        ops |= QFileDialog.DontUseNativeDialog

        new_folder = QFileDialog.getExistingDirectory(
            self, "Pick a folder", "", options=ops
        )
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)

    def copy(self):
        editor = self.tab_view.currentWidget()
        if editor is None:
            return
        editor.copy()

    def compilar(self): ...

    def set_up_body(self):
        # Body

        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        # Side_bar
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet(
            """
            background-color: #2b2b2b;
            """
        )
        side_bar_layout = QHBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # setup labels
        folder_label = QLabel()
        folder_label.setPixmap(
            QPixmap("./src/icons/folder-icon-blue.svg").scaled(QSize(25, 25))
        )
        folder_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        folder_label.setFont(self.window_font)
        folder_label.mousePressEvent = self.show_hide_tab
        side_bar_layout.addWidget(folder_label)
        self.side_bar.setLayout(side_bar_layout)

        body.addWidget(self.side_bar)

        # Split View
        self.hsplit = QSplitter(Qt.Horizontal)

        # frame and layout to hold tree view (file explorer)
        self.tree_frame = QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100, 0)
        self.tree_frame.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet(
            """
            QFrame {
            background-color: #21252b;
            border: none;
            padding: 5px;
            color: #D3D3D3;
            }
            QFrame:hover {
                color: white;
            }
            """
        )

        # Create file system model to show in tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())

        # File system filters
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        # Tree View
        self.tree_view = QTreeView()
        self.tree_view.setFont(self.window_font)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)

        # Context menu
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)

        # Handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Hide header and hide other columns except for name
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        # setup layout
        tree_frame_layout.addWidget(self.tree_view)
        self.tree_frame.setLayout(tree_frame_layout)

        # Tab widget to add editor to
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)

        # Add tree view and tab view to split view
        self.hsplit.addWidget(self.tree_frame)
        self.hsplit.addWidget(self.tab_view)

        body.addWidget(self.hsplit)
        body_frame.setLayout(body)

        self.setCentralWidget(body_frame)

    def close_tab(self, index):
        self.tab_view.removeTab(index)

    def show_hide_tab(self, event): ...

    def tree_view_context_menu(self, position): ...

    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        self.set_new_tab(Path(path))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
