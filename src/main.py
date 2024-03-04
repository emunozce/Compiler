from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFrame,
    QHBoxLayout,
    QSizePolicy,
    QSplitter,
    QFileSystemModel,
    QTreeView,
    QMenu,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QFont

from PyQt5.Qsci import QsciScintilla

import sys
import os
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):  # Constructor
        super(QMainWindow, self).__init__()  # Call the constructor of the parent class
        self.init_ui()  # Call the method to initialize the UI

    def init_ui(self):  # Method to initialize the UI
        self.setWindowTitle("IDE")  # Set the title of the window
        self.resize(900, 700)  # Set the size of the window

        self.setStyleSheet(self.read_styles())

        self.window_font = QFont("Droid Sans Mono", 12)  # Set the font of the window
        self.setFont(self.window_font)  # Set the font of the window

        self.set_up_menu()
        self.set_up_body()

        self.show()

    def read_styles(self):
        with open("src/styles/style.css", "r", encoding="utf-8") as file:
            return file.read()

    def get_editor(self) -> QsciScintilla:
        pass

    def set_up_menu(self):
        menu_bar = self.menuBar()  # Get the menu bar of the window

        # File Menu
        file_menu = menu_bar.addMenu("File")

        # New File
        new_file = file_menu.addAction("New File")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        # Open File
        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        # Open Folder
        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

        # Edit Menu
        edit_menu = menu_bar.addMenu("Edit")

        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)

    def new_file(self):
        pass

    def open_file(self):
        pass

    def open_folder(self):
        pass

    def copy(self):
        pass

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
            border-radius: 5px;
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

        # Add tree view to split view
        self.hsplit.addWidget(self.tree_frame)

        body.addWidget(self.hsplit)
        body_frame.setLayout(body)

        self.setCentralWidget(body_frame)

    def tree_view_context_menu(self, position): ...

    def tree_view_clicked(self): ...


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
