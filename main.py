from tkinter import *
from tkinter import ttk, messagebox
import winreg

class Registry:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Registry")
        self.root.geometry("600x400")