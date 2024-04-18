"""
File that contains the dock panels of the application
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextBrowser, QDockWidget


lexer = []


def set_up_dock_panels(window: QMainWindow):
    """
    Sets up the dock panels of the window

    Args:
        window (QMainWindow): The window where the dock panels will be added

    Returns:
        None
    """

    # Panel for the Lexical Analysis
    lexer_panel = QDockWidget("Lexico", window)
    lexer_panel.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    lexer_widget = QTextBrowser()
    lexer.append(lexer_widget)
    lexer_widget.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    lexer_panel.setWidget(lexer_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, lexer_panel)

    # Panel for the Sintactic Analysis
    sintactic_panel = QDockWidget("Sintactico", window)
    sintactic_panel.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    sintactic_widget = QTextBrowser()
    sintactic_widget.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    sintactic_panel.setWidget(sintactic_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, sintactic_panel)

    # Panel for the Semantic Analysis
    semantic_panel = QDockWidget("Semantico", window)
    semantic_panel.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    semantic_widget = QTextBrowser()
    semantic_widget.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    semantic_panel.setWidget(semantic_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, semantic_panel)

    # Panel for the Hash Table
    hash_table_panel = QDockWidget("Hash Table", window)
    hash_table_panel.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    hash_table_widget = QTextBrowser()
    hash_table_widget.setStyleSheet(
        open("./src/css/style.css", encoding="utf-8").read()
    )
    hash_table_panel.setWidget(hash_table_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, hash_table_panel)

    # Panel for the Intermediate Code
    intermediate_code_panel = QDockWidget("Codigo Intermedio", window)
    intermediate_code_panel.setStyleSheet(
        open("./src/css/style.css", encoding="utf-8").read()
    )
    intermediate_code_widget = QTextBrowser()
    intermediate_code_widget.setStyleSheet(
        open("./src/css/style.css", encoding="utf-8").read()
    )
    intermediate_code_panel.setWidget(intermediate_code_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, intermediate_code_panel)

    # Panel for the Results
    results_panel = QDockWidget("Resultados", window)
    results_panel.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    results_widget = QTextBrowser()
    results_widget.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    results_panel.setWidget(results_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, results_panel)

    # panel for the Lexical Errors
    lexic_err_panel = QDockWidget("Err. Lexicos", window)
    lexic_err_panel.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    lexic_err_widget = QTextBrowser()
    lexer.append(lexic_err_widget)
    lexic_err_widget.setStyleSheet(open("./src/css/style.css", encoding="utf-8").read())
    lexic_err_panel.setWidget(lexic_err_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, lexic_err_panel)

    # Panel for the Sintactic Errors
    sintactic_err_panel = QDockWidget("Err. Sintacticos", window)
    sintactic_err_panel.setStyleSheet(
        open("./src/css/style.css", encoding="utf-8").read()
    )
    sintactic_err_widget = QTextBrowser()
    sintactic_err_widget.setStyleSheet(
        open("./src/css/style.css", encoding="utf-8").read()
    )
    sintactic_err_panel.setWidget(sintactic_err_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, sintactic_err_panel)

    # Panel for the Semantic Errors
    semantic_err_panel = QDockWidget("Err. Semanticos", window)
    semantic_err_panel.setStyleSheet(
        open("./src/css/style.css", encoding="utf-8").read()
    )
    semantic_err_widget = QTextBrowser()
    semantic_err_widget.setStyleSheet(
        open("./src/css/style.css", encoding="utf-8").read()
    )
    semantic_err_panel.setWidget(semantic_err_widget)
    window.addDockWidget(Qt.BottomDockWidgetArea, semantic_err_panel)

    window.tabifyDockWidget(lexer_panel, sintactic_panel)
    window.tabifyDockWidget(sintactic_panel, semantic_panel)
    window.tabifyDockWidget(semantic_panel, hash_table_panel)
    window.tabifyDockWidget(hash_table_panel, intermediate_code_panel)
    window.tabifyDockWidget(intermediate_code_panel, results_panel)
    window.tabifyDockWidget(results_panel, lexic_err_panel)
    window.tabifyDockWidget(lexic_err_panel, sintactic_err_panel)
    window.tabifyDockWidget(sintactic_err_panel, semantic_err_panel)

    # Allow the user to drag out the dock widgets
    window.setDockOptions(QMainWindow.AllowTabbedDocks | QMainWindow.AllowNestedDocks)


def set_lexical_analysis_result():
    lexer[0].setText("Lexical Analysis Result")
    lexer[1].setText("Lexical Errors")
