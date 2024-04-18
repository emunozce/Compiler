"""
This module contains the functions to set up the side bar of the main window.
"""

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QFrame, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap


def set_up_sidebar(window: QMainWindow, body: QFrame):
    """Set up the side bar of the main window."""
    window.side_bar = QFrame()
    window.side_bar.setFrameShape(QFrame.StyledPanel)
    window.side_bar.setFrameShadow(QFrame.Plain)
    window.side_bar.setStyleSheet(
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
    folder_label.setFont(window.window_font)
    folder_label.mousePressEvent = show_hide_tab
    side_bar_layout.addWidget(folder_label)
    window.side_bar.setLayout(side_bar_layout)

    body.addWidget(window.side_bar)


def show_hide_tab(event): ...
