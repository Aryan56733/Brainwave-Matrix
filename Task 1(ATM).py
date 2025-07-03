import tkinter as tk
from tkinter import messagebox

users = {
    "alice": {"pin": "1234", "balance": 1500.0, "history": []},
    "bob": {"pin": "4321", "balance": 500.0, "history": []},
    "charlie": {"pin": "1111", "balance": 1000.0, "history": []},
}

class ATM:
    def __init__(self, root):
        self.root = root
        self.root.title("💳 Python ATM")
        self.root.geometry("350x430")
        self.attempts = 0
        self.current_user = None
        self.login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="👤 Enter Username:", font=("Arial", 14)).pack(pady=10)
        self.user_entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.user_entry.pack(pady=5)
        self.user_entry.focus()

        tk.Label(self.root, text="🔐 Enter PIN:", font=("Arial", 14)).pack(pady=10)
        self.pin_entry = tk.Entry(self.root, show="*", font=("Arial", 14), justify='center')
        self.pin_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.check_login, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=15)

    def check_login(self):
        user = self.user_entry.get().strip().lower()
        pin = self.pin_entry.get().strip()

        if user not in users:
            messagebox.showerror("❌ Error", "Username not found.")
            self.pin_entry.delete(0, tk.END)
            return

        if pin != users[user]["pin"]:
            self.attempts += 1
            if self.attempts >= 3:
                messagebox.showerror("🔒 Locked", "Too many failed attempts. Exiting.")
                self.root.destroy()
            else:
                messagebox.showerror("❌ Invalid PIN", f"Incorrect PIN. Attempts left: {3 - self.attempts}")
                self.pin_entry.delete(0, tk.END)
            return

        self.attempts = 0
        self.current_user = user
        messagebox.showinfo("✅ Success", f"Welcome, {user.capitalize()}!")
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"📋 ATM MENU - {self.current_user.capitalize()}", font=("Arial", 16, "bold")).pack(pady=15)
        
        buttons = [
            ("💰 View Balance", self.view_balance),
            ("➕ Deposit", self.deposit_screen),
            ("➖ Withdraw", self.withdraw_screen),
            ("📄 Transaction History", self.show_history),
            ("🔓 Logout", self.logout)
        ]
        
        for (text, cmd) in buttons:
            tk.Button(self.root, text=text, command=cmd, font=("Arial", 14), width=20, pady=8).pack(pady=5)

    def view_balance(self):
        bal = users[self.current_user]["balance"]
        messagebox.showinfo("💼 Balance", f"Your current balance is: ₹{bal:.2f}")

    def deposit_screen(self):
        self.clear_window()
        tk.Label(self.root, text="➕ Deposit Amount", font=("Arial", 16, "bold")).pack(pady=15)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.amount_entry.pack(pady=10)
        self.amount_entry.focus()
        tk.Button(self.root, text="Deposit", command=self.deposit, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu, font=("Arial", 10)).pack()

    def deposit(self):
        try:
            amt = float(self.amount_entry.get())
            if amt <= 0:
                messagebox.showerror("❌ Error", "Enter a valid amount.")
                return
            users[self.current_user]["balance"] += amt
            users[self.current_user]["history"].append(f"🟢 Deposited ₹{amt:.2f}")
            messagebox.showinfo("✅ Success", f"₹{amt:.2f} deposited successfully.")
            self.main_menu()
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid number.")

    def withdraw_screen(self):
        self.clear_window()
        tk.Label(self.root, text="➖ Withdraw Amount", font=("Arial", 16, "bold")).pack(pady=15)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.amount_entry.pack(pady=10)
        self.amount_entry.focus()
        tk.Button(self.root, text="Withdraw", command=self.withdraw, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu, font=("Arial", 10)).pack()

    def withdraw(self):
        try:
            amt = float(self.amount_entry.get())
            if amt <= 0:
                messagebox.showerror("❌ Error", "Enter a valid amount.")
                return
            if amt > users[self.current_user]["balance"]:
                messagebox.showerror("❌ Error", "Insufficient balance.")
                return
            users[self.current_user]["balance"] -= amt
            users[self.current_user]["history"].append(f"🔴 Withdrew ₹{amt:.2f}")
            messagebox.showinfo("✅ Success", f"₹{amt:.2f} withdrawn successfully.")
            self.main_menu()
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid number.")

    def show_history(self):
        self.clear_window()
        tk.Label(self.root, text="📄 Transaction History", font=("Arial", 16, "bold")).pack(pady=15)
        hist = users[self.current_user]["history"]
        if not hist:
            tk.Label(self.root, text="📭 No transactions yet.", font=("Arial", 12)).pack(pady=10)
        else:
            for t in hist:
                tk.Label(self.root, text=t, font=("Arial", 12)).pack(anchor="w", padx=20)
        tk.Button(self.root, text="Back", command=self.main_menu, font=("Arial", 10)).pack(pady=20)

    def logout(self):
        self.current_user = None
        self.attempts = 0
        messagebox.showinfo("👋 Logged out", "You have been logged out.")
        self.login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    atm = ATM(root)
    root.mainloop()
