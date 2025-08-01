import tkinter as tk
from _db_config import get_conn
from tkinter import messagebox


class RegisterWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.parent = parent
        self.win.title("Register")
        self.win.geometry("500x500")
        self.win.resizable(False, False)

        self.win.grab_set()
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.win)
        frame.pack(expand=True)

        tk.Label(frame, text="Username", font=("segoe UI", 10)).grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
        self.user_entry = tk.Entry(frame, width=25)
        self.user_entry.grid(row=0, column=1, pady=(20, 5), padx=5)

        tk.Label(frame, text="Password", font=("segoe UI", 10)).grid(row=1, column=0, padx=10, pady=(20, 5), sticky="e")
        self.pwd_entry = tk.Entry(frame, width=25)
        self.pwd_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame, text="Confirm Password", font=("segoe UI", 10)).grid(row=2, column=0, padx=10, pady=(20, 5), sticky="e")
        self.cpwd_entry = tk.Entry(frame, width=25)
        self.cpwd_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(frame, text="Create Account", command=self.handle_reg, font=("Segoe UI", 10)).grid(row=3, column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=15)
        self.user_entry.focus()

    def handle_reg(self):
        user = self.user_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        cpwd = self.cpwd_entry.get().strip()

        try:
            with get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM LoginInfo WHERE Username = ?", (user,))
                existing = cursor.fetchone()
                if existing:
                    messagebox.showerror("Error", "The Username already exists!")
                    return

                elif not user or not pwd or not cpwd:
                    messagebox.showerror("Error", "please fill all fields!")

                elif pwd != cpwd:
                    messagebox.showerror("Error", "Passwords do not match!")

                else:
                    cursor.execute("""
                            INSERT INTO LoginInfo (Username, Password)
                            VALUES (?, ?)
                        """, (user, pwd))
                    conn.commit()
                    messagebox.showinfo("Done", "The account successfully created!")
                    self.win.destroy()
                    self.parent.username = user
                    self.parent.deiconify()


        except Exception as e:
            messagebox.showerror("DB Error", f"{e}")

    def close_app(self):
        self.parent.destroy()
