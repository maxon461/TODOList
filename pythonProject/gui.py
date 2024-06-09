import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageChops
import login_process
from verification import send_verification_email
import sqlite3

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

        # Task management frame (hidden initially)
        # Task management frame (hidden initially)
        self.task_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.task_frame.pack_propagate(False)

        self.label_tasks = tk.Label(self.task_frame, text="Your Tasks", font=("Helvetica", 20), fg='#d4d4d4',
                                    bg='#1e1e1e')
        self.label_tasks.pack(pady=10)

        # Listbox for task list
        self.task_listbox = tk.Listbox(self.task_frame, bg='#3c3c3c', fg='#d4d4d4', selectbackground='#007acc')
        self.task_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame for task entry and buttons
        self.task_entry_frame = tk.Frame(self.task_frame, bg='#1e1e1e')
        self.task_entry_frame.pack(fill=tk.X, pady=10)

        self.entry_task = tk.Entry(self.task_entry_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.entry_task.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.button_add_task = tk.Button(self.task_entry_frame, text="Add Task", command=self.add_task, bg='#007acc',
                                         fg='black')
        self.button_add_task.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_delete_task = tk.Button(self.task_entry_frame, text="Delete Task", command=self.delete_task,
                                            bg='#007acc', fg='black')
        self.button_delete_task.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_logout = tk.Button(self.task_entry_frame, text="Logout", command=self.logout, bg='#007acc',
                                       fg='black')
        self.button_logout.pack(side=tk.LEFT, padx=5, pady=5)

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

        # if not login_process.validate_email(username):
        #     messagebox.showerror("Error", "Please enter a valid email address.")
        #     return
        # USE 1 1
        user_id = login_process.login_user(username, password)
        if user_id:
            self.user_id = user_id
            self.load_tasks()
            self.start_frame.pack_forget()
            self.task_frame.pack()
        else:
            messagebox.showerror("Error", "Invalid login credentials. Please try again.")

    def load_tasks(self):
        # Create tasks table if it doesn't exist
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

        # Load tasks for the logged-in user
        self.task_listbox.delete(0, tk.END)
        cursor.execute("SELECT task FROM tasks WHERE user_id=?", (self.user_id,))
        tasks = cursor.fetchall()
        for task in tasks:
            self.task_listbox.insert(tk.END, task[0])
        conn.close()

    def add_task(self):
        task = self.entry_task.get()
        if task:
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (self.user_id, task))
            conn.commit()
            conn.close()
            self.load_tasks()
            self.entry_task.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task = self.task_listbox.get(selected_task_index)
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE user_id=? AND task=?", (self.user_id, selected_task))
            conn.commit()
            conn.close()
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def clear_entries(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_verification.delete(0, tk.END)

    def logout(self):
        self.user_id = None
        self.task_frame.pack_forget()
        self.start_frame.pack()
        self.clear_entries()

def main():
    root = tk.Tk()
    root.geometry("1000x500")
    app = LoginFrame(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()