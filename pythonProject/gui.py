import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import login_process

class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1000, height=500)
        self.master = master
        self.master.title("Login and Register")
        self.pack_propagate(False)  # Prevent the frame from resizing to its contents
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Top label
        self.label_top = tk.Label(self, text="Hi crypto guru! Login or make new account.",
                                  font=("Helvetica", 30, "bold"))
        self.label_top.pack()

        # Username entry
        self.label_username = tk.Label(self, text="Username (Email):")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        # Password entry
        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        # Buttons for registration and login
        self.button_register = tk.Button(self, text="Register", command=self.on_register_click)
        self.button_register.pack()
        self.button_login = tk.Button(self, text="Login", command=self.on_login_click)
        self.button_login.pack()

        # Label for project creator
        self.label_creator = tk.Label(self, text="The project was made by MaxAuto")
        self.label_creator.place(relx=0.9, rely=0.9, anchor="se")  # Place in bottom right corner

        # Load and display the image
        image = Image.open("MaxAuto.png")
        image = image.resize((70, 70), Image.Resampling.BOX)  # Resize the image
        self.maxauto_image = ImageTk.PhotoImage(image)
        self.label_image = tk.Label(self, image=self.maxauto_image)
        self.label_image.place(relx=1.0, rely=1, anchor="se")  # Place near the bottom right corner

        # Place the login process in the center
        self.label_username.place(relx=0.5, rely=0.4, anchor="center")
        self.entry_username.place(relx=0.5, rely=0.45, anchor="center")
        self.label_password.place(relx=0.5, rely=0.5, anchor="center")
        self.entry_password.place(relx=0.5, rely=0.55, anchor="center")
        self.button_register.place(relx=0.45, rely=0.65, anchor="center")
        self.button_login.place(relx=0.55, rely=0.65, anchor="center")

    # Function to handle registration button click
    def on_register_click(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not login_process.validate_email(username):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if not login_process.validate_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and contain at least one capital letter and one number.")
            return

        if login_process.register_user(username, password):
            self.clear_entries()

    # Function to handle login button click
    def on_login_click(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not login_process.validate_email(username):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        login_process.login_user(username, password)

    # Function to clear entry fields
    def clear_entries(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

def main():
    root = tk.Tk()
    root.geometry("1000x500")  # Set the size of the root window
    app = LoginFrame(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()