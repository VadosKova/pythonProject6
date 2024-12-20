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

    def load_root_folders(self):
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

        selected_item = selected_item[0]
        key_name = self.tree.item(selected_item, "text")

        if key_name in ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS",
                        "HKEY_CURRENT_CONFIG"]:
            self.load_subkeys(selected_item, getattr(winreg, key_name), "")
        else:
            parent_item = self.tree.parent(selected_item)
            parent_key_name = self.tree.item(parent_item, "text")
            parent_full_path = self.get_full_path(parent_key_name, key_name)
            self.load_subkeys(selected_item, getattr(winreg, parent_key_name), parent_full_path)

    def load_subkeys(self, parent, hive, subkey):
        for item in self.tree.get_children(parent):
            self.tree.delete(item)

        try:
            key = winreg.OpenKey(hive, subkey)
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    self.tree.insert(parent, "end", subkey_name, text=subkey_name, open=False)
                    i += 1
                except OSError:
                    break
        except FileNotFoundError:
            messagebox.showerror("Error", f"Ключ: {subkey} не найден")
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось открыть ключ: {str(e)}")
        finally:
            try:
                winreg.CloseKey(key)
            except:
                pass

    def get_full_path(self, parent_key_name, folder_name):
        if parent_key_name in ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS",
                               "HKEY_CURRENT_CONFIG"]:
            return folder_name
        else:
            parent_path = self.tree.item(self.tree.parent(self.tree.selection()[0]), "text")
            return parent_path + "\\" + folder_name

    def create_folder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Сначала выберите папку")
            return

        selected_item = selected_item[0]
        parent_key = self.tree.item(selected_item, "text")

        folder_name = "Test"

        try:
            if parent_key in ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS",
                              "HKEY_CURRENT_CONFIG"]:
                key = winreg.OpenKey(getattr(winreg, parent_key), "")
                winreg.CreateKey(key, folder_name)
                messagebox.showinfo("INFO", f"Папка '{folder_name}' создана")
                self.load_subkeys(selected_item, getattr(winreg, parent_key), parent_key)
                winreg.CloseKey(key)
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось создать папку: {str(e)}")

    def write_value(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Сначала выберите папку")
            return

        selected_item = selected_item[0]
        folder_name = self.tree.item(selected_item, "text")

        value_name = "test"
        value_data = "testData"

        try:
            parent_item = self.tree.parent(selected_item)
            parent_key_name = self.tree.item(parent_item, "text")
            parent_full_path = self.get_full_path(parent_key_name, folder_name)
            key = winreg.OpenKey(getattr(winreg, parent_key_name), parent_full_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
            messagebox.showinfo("INFO", f"Значение '{value_name}' записано")
            winreg.CloseKey(key)
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось записать значение: {str(e)}")

    def delete_folder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Выберите папку для удаления")
            return

        selected_item = selected_item[0]
        folder_name = self.tree.item(selected_item, "text")

        confirm = messagebox.askyesno("Удаление папки", f"Удалить '{folder_name}'?")
        if confirm:
            try:
                parent_item = self.tree.parent(selected_item)
                parent_key_name = self.tree.item(parent_item, "text")

                parent_full_path = self.get_full_path(parent_key_name, folder_name)

                key = winreg.OpenKey(getattr(winreg, parent_key_name), parent_full_path, 0, winreg.KEY_SET_VALUE)

                winreg.DeleteKey(key, folder_name)
                winreg.CloseKey(key)

                messagebox.showinfo("INFO", f"Папка '{folder_name}' удалена")

                self.load_subkeys(parent_item, getattr(winreg, parent_key_name), parent_full_path)

            except Exception as e:
                messagebox.showerror("Error", f"Не удалось удалить папку: {str(e)}")


root = Tk()
reg = Registry(root)

root.mainloop()