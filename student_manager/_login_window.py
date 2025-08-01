import tkinter as tk
from tkinter import messagebox
from _db_config import get_conn
from _register_window import RegisterWindow


class LoginWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.parent = parent
        self.win.title("Login")
        self.win.geometry("300x180")
        self.win.resizable(False, False)
        self.win.grab_set()
        self.build_ui()

        # ------  UH DESIGN

    def build_ui(self):
        frame = tk.Frame(self.win)
        frame.pack(expand=True)

        tk.Label(frame, text="Username:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
        self.user_entry = tk.Entry(frame, width=25)
        self.user_entry.grid(row=0, column=1, pady=(20, 5), padx=5)

        tk.Label(frame, text="Password:", font=("Segoe UI", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.pas_entry = tk.Entry(frame, show="*", width=25)
        self.pas_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Button(frame, text="Login", command=self.handle_login, font=("Segoe UI", 10)).grid(row=2, column=0, columnspan=2, pady=15)
        # self.user_entry.focus()

        tk.Button(frame, text="Create Account", command=self.open_reg).grid(row=4, column=0, columnspan=2, pady=15)

    def handle_login(self):
        user = self.user_entry.get().strip()  # removes any leading or trailing whitespace from the input.
        pas = self.pas_entry.get().strip()

        try:
            with get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM LoginInfo WHERE Username=? AND Password=?", (user, pas))
                result = cursor.fetchone()

            if result:
                messagebox.showinfo("Login Success", f"welcome {user}")
                self.win.destroy()
                self.parent.username = user
                self.parent.deiconify()

            elif not user or not pas:
                tk.messagebox.showerror("Validation", "User and Password are required!")

            else:
                messagebox.showerror("Login Failed!", "Invalid username or Password")

        except Exception as e:
            messagebox.showerror("Database Error", f"{e}")

    def open_reg(self):
        RegisterWindow(self.win)

    def close_app(self):
        self.parent.destroy()
