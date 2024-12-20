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

    def load_root_folder(self):
        roots = [
            (winreg.HKEY_CLASSES_ROOT, "HKEY_CLASSES_ROOT"),
            (winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER"),
            (winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE"),
            (winreg.HKEY_USERS, "HKEY_USERS"),
            (winreg.HKEY_CURRENT_CONFIG, "HKEY_CURRENT_CONFIG")
        ]

        for root, name in roots:
            self.tree.insert("", "end", name, text=name, open=True, tags=["root"])

    def open_key(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Выберите ключ для открытия")
            return