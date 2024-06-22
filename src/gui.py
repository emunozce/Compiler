import tkinter as tk
from tkinter import ttk
from lexer import get_lexycal_analysis
from parser_s import Parser
from pathlib import Path

class ASTViewer(tk.Tk):
    def __init__(self, ast):
        super().__init__()
        self.title("AST Viewer")
        self.geometry("600x400")
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.build_tree(ast)

    def build_tree(self, node, parent=""):
        node_id = self.tree.insert(parent, "end", text=f"{node.node_type}({node.value})")
        for child in node.children:
            self.build_tree(child, node_id)

def main(file_path):
    tkns, errs = get_lexycal_analysis(Path(file_path))

    if errs:
        for error in errs:
            print(f"{error}")
    else:
        parser = Parser(tkns)
        try:
            ast = parser.parse()
            print("Parsing successful!")
            app = ASTViewer(ast)
            app.mainloop()
        except SyntaxError as e:
            print(f"Syntax error: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python gui.py <source_file>")
    else:
        main(sys.argv[1])
