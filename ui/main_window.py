# main_window.py
# GUI mit Tkinter (Entry-Felder, Buttons etc.)

import tkinter as tk
from core import db, auth, logic
from tkinter import simpledialog, messagebox, ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("700x400")
        self.username = None
        self.user_id = None
        self.show_login()

    def show_login(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Login or Register", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username:").pack()
        self.login_username = tk.Entry(self.root)
        self.login_username.pack()
        tk.Label(self.root, text="Password:").pack()
        self.login_password = tk.Entry(self.root, show='*')
        self.login_password.pack()
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Login", command=self.handle_login).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Register", command=self.handle_register).pack(side=tk.LEFT, padx=5)
        self.login_status = tk.Label(self.root, text="")
        self.login_status.pack()

    def handle_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if not username or not password:
            self.login_status.config(text="Please enter username and password", fg="red")
            return
        if auth.login_user(username, password):
            self.username = username
            self.user_id = db.get_user_id(username)
            self.show_vault()
        else:
            self.login_status.config(text="Wrong username or password!", fg="red")

    def handle_register(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if not username or not password:
            self.login_status.config(text="Please enter username and password", fg="red")
            return
        if auth.register_user(username, password):
            self.login_status.config(text="Registration successful! You can now log in.", fg="green")
        else:
            self.login_status.config(text="Username already exists!", fg="red")

    def show_vault(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text=f"Welcome, {self.username}", font=("Arial", 14)).pack(pady=5)
        logout_btn = tk.Button(self.root, text="Logout", command=self.logout)
        logout_btn.pack(pady=5)
        # Table for saved passwords
        self.tree = ttk.Treeview(self.root, columns=("Service", "Notes", "Created At"), show='headings')
        self.tree.heading("Service", text="Service")
        self.tree.heading("Notes", text="Notes")
        self.tree.heading("Created At", text="Created At")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_vault_entries()
        add_btn = tk.Button(self.root, text="Add New Password", command=self.add_password_dialog)
        add_btn.pack(pady=5)

    def logout(self):
        self.username = None
        self.user_id = None
        self.show_login()

    def load_vault_entries(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        entries = db.get_entries(self.user_id)
        for entry in entries:
            self.tree.insert('', tk.END, values=(entry[1], entry[3], entry[4]))

    def add_password_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Password")
        dialog.geometry("350x250")
        tk.Label(dialog, text="Service:").pack()
        service_entry = tk.Entry(dialog)
        service_entry.pack()
        tk.Label(dialog, text="Password:").pack()
        password_entry = tk.Entry(dialog, show='*')
        password_entry.pack()
        tk.Label(dialog, text="Notes:").pack()
        notes_entry = tk.Entry(dialog)
        notes_entry.pack()
        status_label = tk.Label(dialog, text="")
        status_label.pack()
        def save():
            service = service_entry.get()
            password = password_entry.get()
            notes = notes_entry.get()
            if not logic.validate_password(password):
                status_label.config(text="Password is too weak!", fg="red")
                return
            try:
                logic.save_password(self.user_id, service, password, notes)
                status_label.config(text="Password saved!", fg="green")
                self.load_vault_entries()
                dialog.destroy()
            except Exception as e:
                status_label.config(text=f"Error: {e}", fg="red")
        tk.Button(dialog, text="Save", command=save).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()