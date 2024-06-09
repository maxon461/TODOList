import tkinter as tk
from tkinter import messagebox
import login_process

# Function to handle registration button click
def on_register_click():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    login_process.register_user(username, password)

# Function to handle login button click
def on_login_click():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    login_process.login_user(username, password)

# Main Tkinter window
def main():
    root = tk.Tk()
    root.title("Login and Register")

    # Username entry
    label_username = tk.Label(root, text="Username:")
    label_username.pack()
    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack()

    # Password entry
    label_password = tk.Label(root, text="Password:")
    label_password.pack()
    global entry_password
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    # Buttons for registration and login
    button_register = tk.Button(root, text="Register", command=on_register_click)
    button_register.pack()
    button_login = tk.Button(root, text="Login", command=on_login_click)
    button_login.pack()

    root.mainloop()

if __name__ == "__main__":
    main()