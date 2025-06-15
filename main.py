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
    # Center the window on the screen
    window_width = 900
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()