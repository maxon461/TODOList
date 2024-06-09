import sqlite3
from tkinter import messagebox
import re

# Function to validate email format
def validate_email(email):
    pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
    return pattern.match(email)

# Function to validate password format
def validate_password(password):
    # At least 8 characters, one capital letter, and one number
    return len(password) >= 8 and any(char.isupper() for char in password) and any(char.isdigit() for char in password)

# Function to create a new user account
def register_user(username, password):
    if not validate_email(username):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return False
    if not validate_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters long and contain at least one capital letter and one number.")
        return False

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose a different one.")
        return False
    finally:
        conn.close()

# Function to authenticate user login
def login_user(username, password):
    if not validate_email(username):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return False

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if c.fetchone() is not None:
        messagebox.showinfo("Success", "Login successful!")
        return True
    else:
        messagebox.showerror("Error", "Invalid username or password.")
        return False
    conn.close()