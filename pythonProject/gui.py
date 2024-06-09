import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageChops
import login_process
from verification import send_verification_email

def crop_image(image_path):
    """
    Crop white borders from the image.
    """
    image = Image.open(image_path)
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    else:
        return image

class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1000, height=500, bg='#1e1e1e')  # Set background to dark
        self.master = master
        self.master.title("Login and Register")
        self.pack_propagate(False)  # Prevent the frame from resizing to its contents
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Main frame (start frame) widgets
        self.start_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.start_frame.pack_propagate(False)
        self.start_frame.pack()

        self.label_top = tk.Label(self.start_frame, text="Hi crypto guru! Login or make new account.", font=("Helvetica", 30, "bold"), fg='#d4d4d4', bg='#1e1e1e')
        self.label_top.pack()

        self.label_username = tk.Label(self.start_frame, text="Username (Email):", fg='#d4d4d4', bg='#1e1e1e')
        self.label_username.pack()
        self.entry_username = tk.Entry(self.start_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.entry_username.pack()

        self.label_password = tk.Label(self.start_frame, text="Password:", fg='#d4d4d4', bg='#1e1e1e')
        self.label_password.pack()
        self.entry_password = tk.Entry(self.start_frame, show="*", bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.entry_password.pack()

        self.button_register = tk.Button(self.start_frame, text="Register", command=self.on_register_click, bg='#007acc', fg='black')
        self.button_register.pack(pady=5)
        self.button_login = tk.Button(self.start_frame, text="Login", command=self.on_login_click, bg='#007acc', fg='black')
        self.button_login.pack(pady=5)

        self.label_creator = tk.Label(self.start_frame, text="The project was made by MaxAuto", fg='#d4d4d4', bg='#1e1e1e')
        self.label_creator.place(relx=0.9, rely=0.9, anchor="se")

        # Crop the image to remove white borders
        cropped_image = crop_image("MaxAuto.png")
        self.maxauto_image = ImageTk.PhotoImage(cropped_image.resize((70, 70), Image.Resampling.BOX))
        self.label_image = tk.Label(self.start_frame, image=self.maxauto_image, bg='#1e1e1e')
        self.label_image.place(relx=1.0, rely=1, anchor="se")

        # Verification frame widgets (hidden initially)
        self.verification_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.verification_frame.pack_propagate(False)

        self.label_verification = tk.Label(self.verification_frame, text="Enter verification code:", fg='#d4d4d4', bg='#1e1e1e')
        self.entry_verification = tk.Entry(self.verification_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.button_verify = tk.Button(self.verification_frame, text="Verify", command=self.on_verify_click, bg='#007acc', fg='black')

        # Grid layout to center widgets in verification frame
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

        # Show verification frame and hide start frame
        self.start_frame.pack_forget()
        self.verification_frame.pack()

    def on_verify_click(self):
        entered_code = self.entry_verification.get()

        if entered_code == self.verification_code:
            # Proceed with registration
            if login_process.register_user(self.email, self.entry_password.get()):
                self.clear_entries()
                self.verification_frame.pack_forget()  # Hide verification frame
                self.start_frame.pack()  # Show start frame again
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