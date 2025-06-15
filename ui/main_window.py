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
        self.apply_darkmode()
        self.show_login()

    def apply_darkmode(self):
        bg = '#222'
        fg = '#f0f0f0'
        self.root.configure(bg=bg)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background=bg, foreground=fg, fieldbackground=bg)
        style.configure('Treeview.Heading', background='#333', foreground=fg)
        # This will be called after widgets are created as well
        self._dark_bg = bg
        self._dark_fg = fg

    def update_widget_colors(self):
        # This method is now redundant since dark mode is always used, but we keep it to ensure all widgets are styled consistently.
        for widget in self.root.winfo_children():
            try:
                if isinstance(widget, tk.Entry):
                    widget.configure(bg='#fff', fg='#000', insertbackground='#000')
                elif isinstance(widget, tk.Button):
                    widget.configure(bg='#fff', fg='#000', activebackground='#ddd', activeforeground='#000', relief=tk.FLAT, borderwidth=0, highlightthickness=0)
                else:
                    widget.configure(bg=self._dark_bg, fg=self._dark_fg)
            except:
                pass

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self._dark_bg)
        container.place(relx=0.5, rely=0.5, anchor='c')
        tk.Label(container, text="Username:", font=("Arial", 16), bg=self._dark_bg, fg=self._dark_fg).pack(pady=(0,4))
        self.login_username = tk.Entry(container, font=("Arial", 16), width=20, bg='#fff', fg='#000', insertbackground='#000')
        self.login_username.pack(pady=(0,10))
        tk.Label(container, text="Password:", font=("Arial", 16), bg=self._dark_bg, fg=self._dark_fg).pack(pady=(0,4))
        self.login_password = tk.Entry(container, show='*', font=("Arial", 16), width=20, bg='#fff', fg='#000', insertbackground='#000')
        self.login_password.pack(pady=(0,16))
        btn_frame = tk.Frame(container, bg=self._dark_bg)
        btn_frame.pack(pady=10)
        login_btn = tk.Button(btn_frame, text="Login", command=self.handle_login, bg='#fff', fg='#000', activebackground='#ddd', activeforeground='#000', relief=tk.FLAT, borderwidth=0, highlightthickness=0, font=("Arial", 14), width=10, height=1)
        login_btn.pack(side=tk.LEFT, padx=10)
        register_btn = tk.Button(btn_frame, text="Register", command=self.handle_register, bg='#fff', fg='#000', activebackground='#ddd', activeforeground='#000', relief=tk.FLAT, borderwidth=0, highlightthickness=0, font=("Arial", 14), width=10, height=1)
        register_btn.pack(side=tk.LEFT, padx=10)
        self.login_status = tk.Label(container, text="", font=("Arial", 14), bg=self._dark_bg, fg=self._dark_fg)
        self.login_status.pack(pady=(10,0))
        self.update_widget_colors()

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
        logout_btn = tk.Button(self.root, text="Logout", command=self.logout, bg='#fff', fg='#000', activebackground='#ddd', activeforeground='#000', relief=tk.FLAT, borderwidth=0, highlightthickness=0, font=("Arial", 12))
        logout_btn.pack(pady=5)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background='#fff', foreground='#000', fieldbackground='#fff')
        style.configure('Treeview.Heading', background='#f0f0f0', foreground='#000')
        self.tree = ttk.Treeview(self.root, columns=("Service", "Notes", "Created At"), show='headings')
        self.tree.heading("Service", text="Service")
        self.tree.heading("Notes", text="Notes")
        self.tree.heading("Created At", text="Created At")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_vault_entries()
        add_btn = tk.Button(self.root, text="Add New Password", command=self.add_password_dialog, bg='#fff', fg='#000', activebackground='#ddd', activeforeground='#000', relief=tk.FLAT, borderwidth=0, highlightthickness=0, font=("Arial", 12))
        add_btn.pack(pady=5)
        self.update_widget_colors()

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
        self.apply_darkmode_to_dialog(dialog)
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

    def apply_darkmode_to_dialog(self, dialog):
        bg = self._dark_bg
        fg = self._dark_fg
        dialog.configure(bg=bg)
        for widget in dialog.winfo_children():
            try:
                if isinstance(widget, tk.Entry):
                    widget.configure(bg='#fff', fg='#000', insertbackground='#000')
                elif isinstance(widget, tk.Button):
                    widget.configure(bg='#fff', fg='#000', activebackground='#ddd', activeforeground='#000')
                else:
                    widget.configure(bg=bg, fg=fg)
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()