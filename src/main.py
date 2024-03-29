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
    QDockWidget,
    QTextBrowser,
)
from PyQt5.QtCore import Qt, QDir, QSize, QModelIndex
from PyQt5.QtGui import QFont, QPixmap, QColor

from PyQt5.Qsci import QsciScintilla

import sys
import os
from pathlib import Path

from editor import Editor


class MainWindow(QMainWindow):
    def __init__(self):  # Constructor
        super(QMainWindow, self).__init__()  # Call the constructor of the parent class
        self.init_ui()  # Call the method to initialize the UI

        self.current_file = None

        self.create_dock_panels()

    def init_ui(self):  # Method to initialize the UI
        self.setWindowTitle("IDE")  # Set the title of the window
        self.resize(1100, 900)  # Set the size of the window

        self.window_font = QFont("Droid Sans Mono", 12)  # Set the font of the window
        self.setFont(self.window_font)  # Set the font of the window

        self.set_up_menu()
        self.set_up_body()

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

    def set_up_menu(self):
        menu_bar = self.menuBar()  # Get the menu bar of the window
        menu_bar.setStyleSheet(open("./src/css/style.css").read())

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

        # Save File
        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        # Save As
        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)

        # Open Folder
        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

        # Edit Menu
        edit_menu = menu_bar.addMenu("Edit")

        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)

        # Compile Menu
        compilar_menu = menu_bar.addMenu("Run")
        compilar_action = compilar_menu.addAction("Start")
        compilar_action.setShortcut("Ctrl+R")
        compilar_action.triggered.connect(self.compilar)

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
        self.current_file.write_text(editor.text())
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
        path.write_text(editor.text())
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

    def create_dock_panels(self):
        # Lexico Panel
        lexico_panel = QDockWidget("Lexico", self)
        lexico_widget = QTextBrowser()
        lexico_panel.setWidget(lexico_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, lexico_panel)

        # Sintactico Panel
        sintactico_panel = QDockWidget("Sintactico", self)
        sintactico_widget = QTextBrowser()
        sintactico_panel.setWidget(sintactico_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, sintactico_panel)

        # Semantico Panel
        semantico_panel = QDockWidget("Semantico", self)
        semantico_widget = QTextBrowser()
        semantico_panel.setWidget(semantico_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, semantico_panel)

        # Hash Table Panel
        hash_table_panel = QDockWidget("Hash Table", self)
        hash_table_widget = QTextBrowser()
        hash_table_panel.setWidget(hash_table_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, hash_table_panel)

        # Codigo Intermedio Panel
        codigo_intermedio_panel = QDockWidget("Codigo Intermedio", self)
        codigo_intermedio_widget = QTextBrowser()
        codigo_intermedio_panel.setWidget(codigo_intermedio_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, codigo_intermedio_panel)

        # Results Panel
        results_panel = QDockWidget("Resultados", self)
        results_widget = QTextBrowser()
        results_panel.setWidget(results_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, results_panel)

        # Lexic Errors Panel
        errores_lexic_panel = QDockWidget("Err. Lexicos", self)
        errores_lexic_widget = QTextBrowser()
        errores_lexic_panel.setWidget(errores_lexic_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, errores_lexic_panel)

        # Sintactic Errors Panel
        errores_sintactic_panel = QDockWidget("Err. Sintacticos", self)
        errores_sintactic_widget = QTextBrowser()
        errores_sintactic_panel.setWidget(errores_sintactic_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, errores_sintactic_panel)

        # Semantic Errors Panel
        errores_semantic_panel = QDockWidget("Err. Semanticos", self)
        errores_semantic_widget = QTextBrowser()
        errores_semantic_panel.setWidget(errores_semantic_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, errores_semantic_panel)

        self.tabifyDockWidget(lexico_panel, sintactico_panel)
        self.tabifyDockWidget(sintactico_panel, semantico_panel)
        self.tabifyDockWidget(semantico_panel, hash_table_panel)
        self.tabifyDockWidget(hash_table_panel, codigo_intermedio_panel)
        self.tabifyDockWidget(codigo_intermedio_panel, results_panel)
        self.tabifyDockWidget(results_panel, errores_lexic_panel)
        self.tabifyDockWidget(errores_lexic_panel, errores_sintactic_panel)
        self.tabifyDockWidget(errores_sintactic_panel, errores_semantic_panel)

        # Allow the user to drag out the dock widgets
        self.setDockOptions(QMainWindow.AllowTabbedDocks | QMainWindow.AllowNestedDocks)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
