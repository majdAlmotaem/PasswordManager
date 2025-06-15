# main_window.py
# GUI mit Tkinter (Entry-Felder, Buttons etc.)

import tkinter as tk
from core import db, auth, logic
from tkinter import ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("900x600")
        self.username = None
        self.accent = '#00BFFF'  # Modern accent color
        self.font = ("Segoe UI", 13)
        self.apply_darkmode()
        self.show_login()

    def apply_darkmode(self):
        bg = '#181c24'  # Glassy dark
        fg = '#f0f0f0'
        self.root.configure(bg=bg)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background=bg, foreground=fg, fieldbackground=bg, bordercolor='#222', rowheight=28, font=self.font)
        style.configure('Treeview.Heading', background='#232837', foreground=self.accent, font=("Segoe UI", 13, "bold"), borderwidth=0)
        style.map('Treeview', background=[('selected', '#222e3c')], foreground=[('selected', self.accent)])
        style.layout('Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])
        self._dark_bg = bg
        self._dark_fg = fg

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self._dark_bg, bd=0, highlightbackground=self.accent, highlightthickness=2)
        container.place(relx=0.5, rely=0.5, anchor='c')
        container.configure(padx=40, pady=30)
        tk.Label(container, text="Welcome to Personal Password Manager", font=("Segoe UI", 18, "bold"), bg=self._dark_bg, fg=self.accent).pack(pady=(0,16))
        tk.Label(container, text="Username:", font=self.font, bg=self._dark_bg, fg=self._dark_fg).pack(pady=(0,4))
        self.login_username = tk.Entry(container, font=self.font, width=22, bg='#232837', fg=self._dark_fg, insertbackground=self.accent, relief=tk.FLAT, highlightthickness=2, highlightbackground=self.accent)
        self.login_username.pack(pady=(0,10))
        tk.Label(container, text="Password:", font=self.font, bg=self._dark_bg, fg=self._dark_fg).pack(pady=(0,4))
        self.login_password = tk.Entry(container, show='*', font=self.font, width=22, bg='#232837', fg=self._dark_fg, insertbackground=self.accent, relief=tk.FLAT, highlightthickness=2, highlightbackground=self.accent)
        self.login_password.pack(pady=(0,16))
        btn_frame = tk.Frame(container, bg=self._dark_bg)
        btn_frame.pack(pady=10)
        login_btn = tk.Button(btn_frame, text="Login", command=self.handle_login, bg=self.accent, fg='#fff', activebackground='#232837', activeforeground=self.accent, relief=tk.FLAT, borderwidth=0, font=self.font, width=12, height=1, cursor="hand2")
        login_btn.pack(side=tk.LEFT, padx=10)
        register_btn = tk.Button(btn_frame, text="Register", command=self.handle_register, bg=self.accent, fg='#fff', activebackground='#232837', activeforeground=self.accent, relief=tk.FLAT, borderwidth=0, font=self.font, width=12, height=1, cursor="hand2")
        register_btn.pack(side=tk.LEFT, padx=10)
        self.login_status = tk.Label(container, text="", font=self.font, bg=self._dark_bg, fg=self._dark_fg)
        self.login_status.pack(pady=(10,0))
        for btn in [login_btn, register_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#232837', fg=self.accent))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.accent, fg='#fff'))

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
        topbar = tk.Frame(self.root, bg=self._dark_bg)
        topbar.pack(fill=tk.X, pady=(0,5))
        tk.Label(topbar, text=f"Welcome, {self.username}", font=("Segoe UI", 15, "bold"), bg=self._dark_bg, fg=self.accent).pack(side=tk.LEFT, padx=10, pady=8)
        add_btn = tk.Button(topbar, text="Add New Password", command=self.add_password_dialog, bg=self.accent, fg='#fff', activebackground='#232837', activeforeground=self.accent, relief=tk.FLAT, borderwidth=0, font=("Segoe UI", 12), cursor="hand2")
        add_btn.pack(side=tk.RIGHT, padx=10, pady=8)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg='#232837', fg=self.accent))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg=self.accent, fg='#fff'))
        card = tk.Frame(self.root, bg='#232837', bd=0, highlightbackground=self.accent, highlightthickness=2)
        card.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        self.tree = ttk.Treeview(card, columns=("Service", "Notes", "Created At"), show='headings', selectmode='browse')
        self.tree.heading("Service", text="Service")
        self.tree.heading("Notes", text="Notes")
        self.tree.heading("Created At", text="Created At")
        self.tree.column("Service", anchor="center")
        self.tree.column("Notes", anchor="center")
        self.tree.column("Created At", anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_vault_entries()
        logout_btn = tk.Button(self.root, text="Logout", command=self.logout, bg=self.accent, fg='#fff', activebackground='#232837', activeforeground=self.accent, relief=tk.FLAT, borderwidth=0, font=("Segoe UI", 12), cursor="hand2")
        logout_btn.pack(pady=5)
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg='#232837', fg=self.accent))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg=self.accent, fg='#fff'))

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
        dialog.geometry("420x320")
        dialog.configure(bg=self._dark_bg)
        # Center the dialog over the main window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 210
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 160
        dialog.geometry(f"420x320+{x}+{y}")
        tk.Label(dialog, text="Service:", font=self.font, bg=self._dark_bg, fg=self._dark_fg).pack(pady=(10,2))
        service_entry = tk.Entry(dialog, font=self.font, bg='#232837', fg=self._dark_fg, insertbackground=self.accent, relief=tk.FLAT, highlightthickness=2, highlightbackground=self.accent)
        service_entry.pack(pady=(0,8))
        tk.Label(dialog, text="Password:", font=self.font, bg=self._dark_bg, fg=self._dark_fg).pack(pady=(0,2))
        password_entry = tk.Entry(dialog, show='*', font=self.font, bg='#232837', fg=self._dark_fg, insertbackground=self.accent, relief=tk.FLAT, highlightthickness=2, highlightbackground=self.accent)
        password_entry.pack(pady=(0,8))
        tk.Label(dialog, text="Notes:", font=self.font, bg=self._dark_bg, fg=self._dark_fg).pack(pady=(0,2))
        notes_entry = tk.Entry(dialog, font=self.font, bg='#232837', fg=self._dark_fg, insertbackground=self.accent, relief=tk.FLAT, highlightthickness=2, highlightbackground=self.accent)
        notes_entry.pack(pady=(0,8))
        status_label = tk.Label(dialog, text="", font=self.font, bg=self._dark_bg, fg=self._dark_fg)
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
        save_btn = tk.Button(dialog, text="Save", command=save, bg=self.accent, fg='#fff', activebackground='#232837', activeforeground=self.accent, relief=tk.FLAT, borderwidth=0, font=self.font, cursor="hand2")
        save_btn.pack(pady=10)
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg='#232837', fg=self.accent))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=self.accent, fg='#fff'))

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()