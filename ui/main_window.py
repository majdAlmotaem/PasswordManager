# main_window.py
# GUI mit Tkinter (Entry-Felder, Buttons etc.)

import tkinter as tk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        # Placeholder for GUI components
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()