# main.py
# Einstiegspunkt, initialisiert GUI & lädt App

from ui.main_window import MainWindow
import tkinter as tk
from core import db
import os

def ensure_data_dir():
    if not os.path.exists('data'):
        os.makedirs('data')

def main():
    ensure_data_dir()
    db.initialize_db()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()