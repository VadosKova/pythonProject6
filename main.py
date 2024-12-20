from tkinter import *
from tkinter import ttk, messagebox
import winreg

class Registry:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Registry")
        self.root.geometry("600x400")

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)

        self.open_btn = Button(self.root, text="Открыть ключ", command=self.open_key)
        self.open_btn.pack(side="left", padx=10, pady=10)

        self.create_folder_btn = Button(self.root, text="Создать папку", command=self.create_folder)
        self.create_folder_btn.pack(side="left", padx=10, pady=10)

        self.write_value_btn = Button(self.root, text="Записать значение", command=self.write_value)
        self.write_value_btn.pack(side="left", padx=10, pady=10)

        self.delete_folder_btn = Button(self.root, text="Удалить папку", command=self.delete_folder)
        self.delete_folder_btn.pack(side="left", padx=10, pady=10)

        self.load_root_folders()