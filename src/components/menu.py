"""
File with the functions to set up the menu bar of the window
"""

from PyQt5.QtWidgets import QMainWindow, QMenu, QAction
from PyQt5.QtGui import QIcon


def set_up_file_menu_actions(window: QMainWindow, file_menu: QMenu):
    """
    Sets up the actions of the file menu

    Args:
        window (QMainWindow): The window where the file will be opened
        file_menu (QMenu): The menu where the actions will be added

    Returns:
        None
    """

    # New File
    new_file = file_menu.addAction("New File")
    new_file.setShortcut("Ctrl+N")
    new_file.triggered.connect(window.new_file)

    # Open File
    open_file = file_menu.addAction("Open File")
    open_file.setShortcut("Ctrl+O")
    open_file.triggered.connect(window.open_file)

    # Save File
    save_file = file_menu.addAction("Save")
    save_file.setShortcut("Ctrl+S")
    save_file.triggered.connect(window.save_file)

    # Save As
    save_as = file_menu.addAction("Save As")
    save_as.setShortcut("Ctrl+Shift+S")
    save_as.triggered.connect(window.save_as)

    # Open Folder
    open_folder = file_menu.addAction("Open Folder")
    open_folder.setShortcut("Ctrl+K")
    open_folder.triggered.connect(window.open_folder)


def set_up_edit_menu_actions(window: QMainWindow, edit_menu: QMenu):
    """
    Sets up the actions of the edit menu

    Args:
        window (QMainWindow): The window where the file will be opened
        edit_menu (QMenu): The menu where the actions will be added

    Returns:
        None
    """

    # Copy
    copy = edit_menu.addAction("Copy")
    copy.setShortcut("Ctrl+C")
    copy.triggered.connect(window.copy)


def set_up_run_menu_actions(window: QMainWindow, run_menu: QMenu):
    """
    Sets up the actions of the run menu

    Args:
        window (QMainWindow): The window where the file will be opened
        run_menu (QMenu): The menu where the actions will be added

    Returns:
        None
    """

    # Compile
    compile_start = run_menu.addAction("Compile")
    compile_start.setShortcut("Ctrl+R")
    compile_start.triggered.connect(window.compile)


def set_up_icons_for_menu(window: QMainWindow, menu_bar):
    """
    Sets up the icons for the menu bar

    Args:
        window (QMainWindow): The window where the file will be opened
        menu_bar (QMenuBar): The menu bar where the icons will be added

    Returns:
        None
    """
    new_file_icon = QAction(QIcon("src/icons/new_file.svg"), "", parent=window)
    new_file_icon.triggered.connect(window.new_file)
    menu_bar.addAction(new_file_icon)

    open_file_icon = QAction(QIcon("src/icons/open_file.svg"), "", parent=window)
    open_file_icon.triggered.connect(window.open_file)
    menu_bar.addAction(open_file_icon)

    save_file_icon = QAction(QIcon("src/icons/save.svg"), "", parent=window)
    save_file_icon.triggered.connect(window.save_file)
    menu_bar.addAction(save_file_icon)

    save_as_icon = QAction(QIcon("src/icons/save_as.svg"), "", parent=window)
    save_as_icon.triggered.connect(window.save_as)
    menu_bar.addAction(save_as_icon)

    open_folder_icon = QAction(QIcon("src/icons/open_folder.svg"), "", parent=window)
    open_folder_icon.triggered.connect(window.open_folder)
    menu_bar.addAction(open_folder_icon)

    compile_icon = QAction(QIcon("src/icons/compile.svg"), "", parent=window)
    compile_icon.triggered.connect(window.compile)
    menu_bar.addAction(compile_icon)


def set_up_menu(window: QMainWindow):
    """
    Builds the menu bar of the window

    Params:
        window (QMainWindow): The window where the menu will be added

    Returns: None
    """
    menu_bar = window.menuBar()  # Get the menu bar of the window
    menu_bar.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())

    # File Menu
    set_up_file_menu_actions(window, menu_bar.addMenu("File"))

    # Edit Menu
    set_up_edit_menu_actions(window, menu_bar.addMenu("Edit"))

    # Compile Menu
    set_up_run_menu_actions(window, menu_bar.addMenu("Run"))

    # Icons
    set_up_icons_for_menu(window, menu_bar)
