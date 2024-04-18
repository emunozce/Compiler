"""
File with the functions to set up the menu bar of the window
"""

from PyQt5.QtWidgets import QMainWindow, QMenu


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
    edit_menu = menu_bar.addMenu("Edit")

    copy_action = edit_menu.addAction("Copy")
    copy_action.setShortcut("Ctrl+C")
    copy_action.triggered.connect(window.copy)

    # Compile Menu
    compilar_menu = menu_bar.addMenu("Run")
    compilar_action = compilar_menu.addAction("Start")
    compilar_action.setShortcut("Ctrl+R")
    compilar_action.triggered.connect(window.compilar)


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
