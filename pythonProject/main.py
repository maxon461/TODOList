import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to create a new user account
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose a different one.")
    conn.close()

# Function to authenticate user login
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if c.fetchone() is not None:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password.")
    conn.close()

# Main Tkinter window
root = tk.Tk()
root.title("Login and Register")

# Username entry
label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

# Password entry
label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Buttons for registration and login
button_register = tk.Button(root, text="Register", command=register_user)
button_register.pack()
button_login = tk.Button(root, text="Login", command=login_user)
button_login.pack()

root.mainloop()