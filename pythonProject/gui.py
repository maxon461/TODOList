import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from PIL import Image, ImageTk, ImageChops
import sqlite3
import login_process
from verification import send_verification_email
from binance.client import Client
from p2p import *
from databases import setup_database


class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1000, height=500, bg='#1e1e1e')
        self.master = master
        self.master.title("Login and Register")
        self.pack_propagate(False)
        self.pack()
        self.user_id = None  # Store the logged-in user's ID
        self.selected_task_text = None  # Store the text of the currently selected task
        self.platform_type = None
        self.create_widgets()

    def create_widgets(self):
        # Main frame (start frame) widgets
        # --------------------------------------------------------------

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

        # --------------------------------------------------------------

        # Verification frame widgets (hidden initially)
        # --------------------------------------------------------------

        self.verification_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.verification_frame.pack_propagate(False)

        self.label_verification = tk.Label(self.verification_frame, text="Enter verification code:", fg='#d4d4d4', bg='#1e1e1e')
        self.entry_verification = tk.Entry(self.verification_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.button_verify = tk.Button(self.verification_frame, text="Verify", command=self.on_verify_click, bg='#007acc', fg='black')

        self.verification_frame.grid_rowconfigure(0, weight=1)
        self.verification_frame.grid_rowconfigure(3, weight=1)
        self.verification_frame.grid_columnconfigure(0, weight=1)
        self.verification_frame.grid_columnconfigure(2, weight=1)

        self.label_verification.grid(row=1, column=1, pady=10)
        self.entry_verification.grid(row=2, column=1, pady=10)
        self.button_verify.grid(row=3, column=1, pady=10)

        # --------------------------------------------------------------

        # Task management frame (hidden initially)
        # --------------------------------------------------------------

        self.task_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.task_frame.pack_propagate(False)

        # Layout with grid
        self.task_frame.grid_rowconfigure(0, weight=1)
        self.task_frame.grid_columnconfigure(0, weight=1)
        self.task_frame.grid_columnconfigure(1, weight=1)

        self.label_tasks = tk.Label(self.task_frame, text="Your Tasks", font=("Helvetica", 20), fg='#d4d4d4', bg='#1e1e1e')
        self.label_tasks.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.button_crypto = tk.Button(self.task_frame, text="CRYPTO", command=self.show_crypto_frame, bg='#007acc', fg='black')
        self.button_crypto.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        # Frame for task list
        self.task_list_frame = tk.Frame(self.task_frame, bg='#1e1e1e')
        self.task_list_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        # Frame for task entry and buttons
        self.task_entry_frame = tk.Frame(self.task_frame, bg='#1e1e1e')
        self.task_entry_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.entry_task = tk.Entry(self.task_entry_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.entry_task.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_add_task = tk.Button(self.task_entry_frame, text="Add Task", command=self.add_task, bg='#007acc', fg='black')
        self.button_add_task.grid(row=0, column=1, padx=5, pady=5)

        self.button_delete_task = tk.Button(self.task_entry_frame, text="Delete Task", command=self.delete_task, bg='#007acc', fg='black')
        self.button_delete_task.grid(row=0, column=2, padx=5, pady=5)

        self.button_logout = tk.Button(self.task_entry_frame, text="Logout", command=self.logout, bg='#007acc', fg='black')
        self.button_logout.grid(row=0, column=3, padx=5, pady=5, sticky="e")

        self.task_entry_frame.grid_columnconfigure(0, weight=1)

        # --------------------------------------------------------------

        # Crypto frame (hidden initially)
        # --------------------------------------------------------------
        self.crypto_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.crypto_frame.pack_propagate(False)

        self.label_crypto = tk.Label(self.crypto_frame, text="Choose your Platform", font=("Helvetica", 20), fg='#d4d4d4', bg='#1e1e1e')
        self.label_crypto.pack(pady=10)

        self.button_okx = tk.Button(self.crypto_frame, text="OKX", command=lambda: self.choose_platform("OKX"), bg='#007acc', fg='black')
        self.button_okx.pack(pady=10)

        self.button_binance = tk.Button(self.crypto_frame, text="Binance", command=lambda: self.choose_platform("Binance"), bg='#007acc', fg='black')
        self.button_binance.pack(pady=10)

        self.button_back_to_list_from_crypto = tk.Button(self.crypto_frame, text="Back to List", command=self.back_to_list, bg='#007acc', fg='black')
        self.button_back_to_list_from_crypto.pack(pady=10)

        # --------------------------------------------------------------

        # API key frame (hidden initially)
        # --------------------------------------------------------------
        self.api_key_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.api_key_frame.pack_propagate(False)

        self.label_api = tk.Label(self.api_key_frame, text="Provide your API and Secret Key", font=("Helvetica", 20), fg='#d4d4d4', bg='#1e1e1e')
        self.label_api.pack(pady=10)

        self.label_api_key = tk.Label(self.api_key_frame, text="API Key:", fg='#d4d4d4', bg='#1e1e1e')
        self.label_api_key.pack()
        self.entry_api_key = tk.Entry(self.api_key_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.entry_api_key.pack()

        self.label_secret_key = tk.Label(self.api_key_frame, text="Secret Key:", fg='#d4d4d4', bg='#1e1e1e')
        self.label_secret_key.pack()
        self.entry_secret_key = tk.Entry(self.api_key_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.entry_secret_key.pack()

        self.button_save_keys = tk.Button(self.api_key_frame, text="Save Keys", command=self.save_api_keys, bg='#007acc', fg='black')
        self.button_save_keys.pack(pady=10)

        self.button_back_to_list_from_api = tk.Button(self.api_key_frame, text="Back to List", command=self.back_to_list, bg='#007acc', fg='black')
        self.button_back_to_list_from_api.pack(pady=10)

        # --------------------------------------------------------------

        # Action selection frame (hidden initially)
        # --------------------------------------------------------------
        self.action_frame = tk.Frame(self, width=1000, height=500, bg='#1e1e1e')
        self.action_frame.pack_propagate(False)

        self.label_action = tk.Label(self.action_frame, text="Choose your Action", font=("Helvetica", 20), fg='#d4d4d4', bg='#1e1e1e')
        self.label_action.grid(row=0, column=0, columnspan=2, pady=10)

        # Spot value of crypto section with Entry
        self.label_spot_value = tk.Button(self.action_frame, text="Spot value of crypto", command=self.spot_value,  bg='#007acc', fg='black')
        self.label_spot_value.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.entry_currency = tk.Entry(self.action_frame, bg='#3c3c3c', fg='#d4d4d4', insertbackground='white')
        self.entry_currency.grid(row=1, column=1, padx=10, pady=10, sticky='e')

        # My spot balance button
        self.button_spot_balance = tk.Button(self.action_frame, text="My spot balance", command=self.spot_balance, bg='#007acc', fg='black')
        self.button_spot_balance.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')

        # P2P daily report button
        self.button_p2p_report = tk.Button(self.action_frame, text="P2P daily report", command=self.p2p_report, bg='#007acc', fg='black')
        self.button_p2p_report.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')


        self.button_back_to_list_from_action = tk.Button(self.action_frame, text="Back to List", command=self.back_to_list, bg='#007acc', fg='black')
        self.button_back_to_list_from_action.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')

    def back_to_list(self):
        self.crypto_frame.pack_forget()
        self.api_key_frame.pack_forget()
        self.action_frame.pack_forget()
        self.task_frame.pack()

    def show_crypto_frame(self):
        self.task_frame.pack_forget()
        self.crypto_frame.pack()

    def choose_platform(self, platform):
        self.platform_type = platform
        self.crypto_frame.pack_forget()

        # Check if API keys exist for this user and platform
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT api_key, secret_key FROM api_keys WHERE user_id=? AND platform_type=?", (self.user_id, self.platform_type))
        keys = cursor.fetchone()
        conn.close()

        if keys:
            messagebox.showinfo("Info", f"API keys for {platform} already exist.")
            self.show_action_frame()
        else:
            self.api_key_frame.pack()

    def save_api_keys(self):
        api_key = self.entry_api_key.get()
        secret_key = self.entry_secret_key.get()

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO api_keys (user_id, platform_type, api_key, secret_key) VALUES (?, ?, ?, ?)",
                       (self.user_id, self.platform_type, api_key, secret_key))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "API keys saved successfully.")
        self.api_key_frame.pack_forget()
        self.show_action_frame()

    def show_action_frame(self):
        self.action_frame.pack()

    def spot_value(self):
        coin_name = self.entry_currency.get().upper()
        if not coin_name:
            messagebox.showerror("Error", "Please enter a valid coin name.")
            return

        # Get the API key and secret key from the database
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT api_key, secret_key FROM api_keys WHERE user_id=? AND platform_type=?", (self.user_id, 'Binance'))
        keys = cursor.fetchone()
        conn.close()

        if not keys:
            messagebox.showerror("Error", "API keys not found.")
            return

        api_key, secret_key = keys
        client = Client(api_key, secret_key)

        try:
            symbol = f"{coin_name}USDT"
            ticker = client.get_symbol_ticker(symbol=symbol)
            price = ticker['price']
            messagebox.showinfo("Spot Value", f"The spot value of {coin_name} is {price} USDT.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve spot value: {e}")

    def spot_balance(self):
        # Get the API key and secret key from the database
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT api_key, secret_key FROM api_keys WHERE user_id=? AND platform_type=?",
                       (self.user_id, 'Binance'))
        keys = cursor.fetchone()
        conn.close()

        if not keys:
            messagebox.showerror("Error", "API keys not found.")
            return

        api_key, secret_key = keys
        client = Client(api_key, secret_key)

        try:
            account_info = client.get_account()
            balances = account_info['balances']
            spot_balances = {balance['asset']: balance['free'] for balance in balances if float(balance['free']) > 0}

            if spot_balances:
                balance_info = "\n".join([f"{asset}: {amount}" for asset, amount in spot_balances.items()])
                messagebox.showinfo("Spot Balances", balance_info)
            else:
                messagebox.showinfo("Spot Balances", "No balances available.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve spot balances: {e}")

    def p2p_report(self):
        # Get the API key and secret key from the database
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT api_key, secret_key FROM api_keys WHERE user_id=? AND platform_type=?",
                       (self.user_id, 'Binance'))
        keys = cursor.fetchone()
        conn.close()

        if not keys:
            messagebox.showerror("Error", "API keys not found.")
            return

        api_key, secret_key = keys
        c2c_order_history = get_binance_c2c_order_history(api_key, secret_key)
        # print(c2c_order_history)
        if c2c_order_history:
            # Parse orders
            c2c_order_data = c2c_order_history.get("data", [])
            parsed_orders = []
            yesterday = (datetime.today() - timedelta(days=1)).date()  # Get yesterday's date

            for order_info in c2c_order_data:
                create_time_milliseconds = order_info.get("createTime")
                create_time_seconds = create_time_milliseconds / 1000
                create_time = datetime.utcfromtimestamp(create_time_seconds + 3600)

                # Check if the order was created yesterday
                if create_time.date() == yesterday:
                    parsed_order = {
                        "orderStatus": order_info.get("orderStatus"),
                        "totalPrice": order_info.get("totalPrice"),
                        "tradeType": order_info.get("tradeType"),
                        "createTime": create_time.strftime('%Y-%m-%d %H:%M:%S')  # Convert to human-readable format
                    }
                    parsed_orders.append(parsed_order)

            profit = count_profit(parsed_orders)
            # Save parsed orders to Excel file
            buy_orders, sell_orders = separate_buy_sell(parsed_orders)
            save_to_excel(buy_orders, sell_orders, profit, f"P2P_History_Yesterday{self.platform_type}.xlsx")
            messagebox.showinfo("Success!", "Parsed orders saved to P2P_History_Yesterday.xlsx")
        else:
            messagebox.showerror("Error", "Failed to retrieve order history")

    def on_register_click(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not login_process.validate_email(username):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if not login_process.validate_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and contain at least one capital letter and one number.")
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

        # Clear previous tasks
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        # Load tasks for the logged-in user
        cursor.execute("SELECT task FROM tasks WHERE user_id=?", (self.user_id,))
        tasks = cursor.fetchall()
        for task in tasks:
            self.create_task_label(task[0])
        conn.close()

    def create_task_label(self, task):
        task_label = tk.Label(self.task_list_frame, text=task, font=("Helvetica", 14), bg='#3c3c3c', fg='#d4d4d4', padx=10, pady=5)
        task_label.pack(fill=tk.X, pady=5)
        task_label.bind("<Button-1>", lambda e: self.select_task(task_label))

        # Restore selection if this was the selected task
        if task == self.selected_task_text:
            self.select_task(task_label)

    def select_task(self, task_label):
        if self.selected_task_text:
            for widget in self.task_list_frame.winfo_children():
                if widget.cget("text") == self.selected_task_text:
                    widget.config(bg='#3c3c3c')
        self.selected_task_text = task_label.cget("text")
        task_label.config(bg='#007acc')

    def delete_task(self):
        if self.selected_task_text:
            task = self.selected_task_text
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE user_id=? AND task=?", (self.user_id, task))
            conn.commit()
            conn.close()
            self.load_tasks()
            self.selected_task_text = None
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

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

    def logout(self):
        self.user_id = None
        self.task_frame.pack_forget()
        self.start_frame.pack()
        self.clear_entries()

    def clear_entries(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_verification.delete(0, tk.END)
        self.entry_task.delete(0, tk.END)

def crop_image(image_path):
    image = Image.open(image_path)
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    else:
        return image

def main():
    setup_database()
    root = tk.Tk()
    root.geometry("1000x500")
    app = LoginFrame(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
