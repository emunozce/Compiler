import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


class SimpleIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Python IDE")

        self.text_editor = tk.Text(root, wrap="word", undo=True, autoseparators=True)
        self.text_editor.pack(expand=True, fill="both")

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_editor.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_editor.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)

    def new_file(self):
        self.text_editor.delete(1.0, tk.END)
        self.root.title("Untitled")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)
                self.root.title(file_path)

    def save_file(self):
        if self.root.title().endswith("Untitled"):
            self.save_as_file()
        else:
            file_path = self.root.title()[22:]
            with open(file_path, "w") as file:
                file.write(self.text_editor.get(1.0, tk.END))

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_editor.get(1.0, tk.END))
            self.root.title("Simple Python IDE - " + file_path)

    def cut_text(self):
        self.text_editor.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_editor.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_editor.event_generate("<<Paste>>")


if __name__ == "__main__":
    root = tk.Tk()
    ide = SimpleIDE(root)
    root.mainloop()
