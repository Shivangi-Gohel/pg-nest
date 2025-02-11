import tkinter as tk
import sqlite3
import re
from tkinter import messagebox
from models.user_model import UserModel
from gui.admin_gui import AdminGUI
from gui.guest_gui import GuestGUI


class LoginGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PG Management System - Login")
        self.window.geometry("600x400")
        self.window.configure(bg="#f0f0f0")  # Light background color

        self.user_model = UserModel()

    def run(self):
        self.login_screen()
        self.window.mainloop()

    def login_screen(self):
        tk.Label(self.window, text="Login", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        frame = tk.Frame(self.window, bg="#ffffff", padx=20, pady=20, relief=tk.GROOVE, bd=2)
        frame.pack(pady=10)

        tk.Label(frame, text="Email:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(frame, font=("Arial", 12))
        email_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(frame, show="*", font=("Arial", 12))
        password_entry.grid(row=1, column=1, pady=5)

        def clear_fields():
            """ Clears the email and password fields. """
            email_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

        def login(event=None):
            email = email_entry.get()
            password = password_entry.get()

            if not email or not password:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            user_type = self.user_model.authenticate_user(email, password)

            if user_type == "admin":
                messagebox.showinfo("Login Successful", "Welcome Admin!")
                clear_fields()  # Clear fields before proceeding
                self.window.withdraw()
                AdminGUI(self.window).run()
            elif user_type == "guest":
                messagebox.showinfo("Login Successful", "Welcome Guest!")
                guest_id = self.get_guest_id(email)
                clear_fields()  # Clear fields before proceeding
                self.window.withdraw()
                GuestGUI(guest_id, self.window).run()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials!")
                clear_fields()  # Clear fields on failed login

        tk.Button(frame, text="Login", command=login, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=2, columnspan=2, pady=10)
        tk.Button(self.window, text="Sign Up", command=self.signup_screen, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=5)

        self.window.bind('<Return>', login)

   
    def get_guest_id(self, email):
        connection = sqlite3.connect("db/pg_management.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id = cursor.fetchone()
        connection.close()
        return user_id[0] if user_id else None

    def signup_screen(self):
        self.window.destroy()
        signup_window = tk.Tk()
        signup_window.title("Sign Up")
        signup_window.geometry("400x500")
        signup_window.configure(bg="#f0f0f0")

        tk.Label(signup_window, text="Sign Up", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        frame = tk.Frame(signup_window, bg="#ffffff", padx=20, pady=20, relief=tk.GROOVE, bd=2)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(frame, font=("Arial", 12))
        name_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(frame, font=("Arial", 12))
        email_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Phone:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        phone_entry = tk.Entry(frame, font=("Arial", 12))
        phone_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Address:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        address_entry = tk.Entry(frame, font=("Arial", 12))
        address_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(frame, show="*", font=("Arial", 12))
        password_entry.grid(row=4, column=1, pady=5)

        def is_valid_email(email):
            return re.match(r"[^@]+@[^@]+\.[^@]+", email)

        def is_valid_password(password):
            return len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"[0-9]", password) and re.search(r"[@$!%*?&]", password)

        def signup(event=None):
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()
            password = password_entry.get()

            if not all([name, email, phone, address, password]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            if not is_valid_email(email):
                messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
                return

            if not is_valid_password(password):
                messagebox.showwarning("Weak Password", "Password must be at least 8 characters long, contain uppercase, lowercase, digits, and special characters.")
                return

            if self.user_model.create_user(name, email, phone, address, password):
                messagebox.showinfo("Sign Up Successful", "You can now log in!")
                signup_window.destroy()
                self.__init__()  # Reinitialize the login window
                self.run()
            else:
                messagebox.showerror("Sign Up Failed", "User already exists!")

        tk.Button(frame, text="Sign Up", command=signup, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=5, columnspan=2, pady=10)
        tk.Button(signup_window, text="Back to Login", command=lambda: [signup_window.destroy(), self.__init__(), self.run()], font=("Arial", 12), bg="#FF5722", fg="white").pack(pady=5)

        signup_window.bind('<Return>', signup)

        signup_window.mainloop()
