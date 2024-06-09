import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import login_process
from verification import send_verification_email

class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1000, height=500)
        self.master = master
        self.master.title("Login and Register")
        self.pack_propagate(False)  # Prevent the frame from resizing to its contents
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Registration frame widgets
        self.label_top = tk.Label(self, text="Hi crypto guru! Login or make new account.", font=("Helvetica", 30, "bold"))
        self.label_top.pack()

        self.label_username = tk.Label(self, text="Username (Email):")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.button_register = tk.Button(self, text="Register", command=self.on_register_click)
        self.button_register.pack()
        self.button_login = tk.Button(self, text="Login", command=self.on_login_click)
        self.button_login.pack()

        self.label_creator = tk.Label(self, text="The project was made by MaxAuto")
        self.label_creator.place(relx=0.9, rely=0.9, anchor="se")

        self.maxauto_image = ImageTk.PhotoImage(Image.open("MaxAuto.png").resize((70, 70), Image.Resampling.BOX))
        self.label_image = tk.Label(self, image=self.maxauto_image)
        self.label_image.place(relx=1.0, rely=1, anchor="se")

        # Verification frame widgets (hidden initially)
        self.verification_frame = tk.Frame(self.master, width=1000, height=500)
        self.verification_frame.pack_propagate(False)

        self.label_verification = tk.Label(self.verification_frame, text="Enter verification code:")
        self.entry_verification = tk.Entry(self.verification_frame)
        self.button_verify = tk.Button(self.verification_frame, text="Verify", command=self.on_verify_click)

        # Grid layout to center widgets
        self.verification_frame.grid_rowconfigure(0, weight=1)
        self.verification_frame.grid_rowconfigure(3, weight=1)
        self.verification_frame.grid_columnconfigure(0, weight=1)
        self.verification_frame.grid_columnconfigure(2, weight=1)

        self.label_verification.grid(row=1, column=1, pady=10)
        self.entry_verification.grid(row=2, column=1, pady=10)
        self.button_verify.grid(row=3, column=1, pady=10)

    def on_register_click(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not login_process.validate_email(username):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if not login_process.validate_password(password):
            messagebox.showerror("Error",
                                 "Password must be at least 8 characters long and contain at least one capital letter and one number.")
            return

        # Send verification email
        self.email = username
        self.verification_code = send_verification_email(username)

        # Show verification frame and hide registration frame
        self.pack_forget()
        self.verification_frame.pack()

    def on_verify_click(self):
        entered_code = self.entry_verification.get()

        if entered_code == self.verification_code:
            # Proceed with registration
            if login_process.register_user(self.email, self.entry_password.get()):
                self.clear_entries()
                self.verification_frame.pack_forget()  # Hide verification frame
                self.pack()  # Show registration frame again
        else:
            messagebox.showerror("Error", "Invalid verification code. Please try again.")

    def on_login_click(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not login_process.validate_email(username):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        login_process.login_user(username, password)

    def clear_entries(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_verification.delete(0, tk.END)

def main():
    root = tk.Tk()
    root.geometry("1000x500")
    app = LoginFrame(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()