import tkinter as tk
from tkinter import messagebox, simpledialog

# These are the  ID's of Dummy users for  authentication
users = {
    "admin": "admin123",
    "user1": "pass1"
}

class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Inventory Management System")
        self.root.geometry("600x500")
        self.logged_user = None

        self.products = {}

        self.login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="🔑 Login", font=("Arial", 20, "bold")).pack(pady=30)

        tk.Label(self.root, text="Username:", font=("Arial", 14)).pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5)
        self.username_entry.focus()

        tk.Label(self.root, text="Password:", font=("Arial", 14)).pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.check_login).pack(pady=20)

    def check_login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()
        if user in users and users[user] == pwd:
            self.logged_user = user
            messagebox.showinfo("✅ Success", f"Welcome, {user}!")
            self.main_menu()
        else:
            messagebox.showerror("❌ Login Failed", "Invalid username or password.")

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"📋 Inventory - User: {self.logged_user}", font=("Arial", 16, "bold")).pack(pady=15)

        btns = [
            ("➕ Add Product", self.add_product),
            ("✏️ Edit Product", self.edit_product),
            ("🗑️ Delete Product", self.delete_product),
            ("📦 View Inventory", self.view_inventory),
            ("⚠️ Low Stock Alert", self.low_stock_alert),
            ("💰 Simulate Sale", self.simulate_sale),
            ("🔓 Logout", self.logout),
        ]

        for (txt, cmd) in btns:
            tk.Button(self.root, text=txt, command=cmd, font=("Arial", 14), width=20, pady=8).pack(pady=5)

    def add_product(self):
        name = simpledialog.askstring("➕ Add Product", "Enter product name:").strip()
        if not name:
            return
        if name in self.products:
            messagebox.showerror("❌ Error", "Product already exists!")
            return
        try:
            price = float(simpledialog.askstring("Price", "Enter product price:"))
            qty = int(simpledialog.askstring("Quantity", "Enter product quantity:"))
            if price < 0 or qty < 0:
                raise ValueError
        except:
            messagebox.showerror("❌ Error", "Invalid price or quantity!")
            return
        self.products[name] = {"price": price, "qty": qty}
        messagebox.showinfo("✅ Added", f"Product '{name}' added successfully.")

    def edit_product(self):
        if not self.products:
            messagebox.showinfo("📭 Empty", "No products to edit.")
            return
        name = simpledialog.askstring("✏️ Edit Product", "Enter product name to edit:").strip()
        if name not in self.products:
            messagebox.showerror("❌ Error", "Product not found!")
            return
        product = self.products[name]
        price = simpledialog.askstring("Price", f"Current price: {product['price']}. Enter new price or leave empty:")
        qty = simpledialog.askstring("Quantity", f"Current qty: {product['qty']}. Enter new quantity or leave empty:")
        try:
            if price:
                price = float(price)
                if price < 0:
                    raise ValueError
                product['price'] = price
            if qty:
                qty = int(qty)
                if qty < 0:
                    raise ValueError
                product['qty'] = qty
        except:
            messagebox.showerror("❌ Error", "Invalid input!")
            return
        messagebox.showinfo("✅ Updated", f"Product '{name}' updated.")

    def delete_product(self):
        if not self.products:
            messagebox.showinfo("📭 Empty", "No products to delete.")
            return
        name = simpledialog.askstring("🗑️ Delete Product", "Enter product name to delete:").strip()
        if name not in self.products:
            messagebox.showerror("❌ Error", "Product not found!")
            return
        confirm = messagebox.askyesno("⚠️ Confirm Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            del self.products[name]
            messagebox.showinfo("🗑️ Deleted", f"Product '{name}' deleted.")

    def view_inventory(self):
        self.clear_window()
        tk.Label(self.root, text="📦 Current Inventory", font=("Arial", 16, "bold")).pack(pady=15)
        if not self.products:
            tk.Label(self.root, text="📭 No products in inventory.", font=("Arial", 14)).pack(pady=10)
        else:
            for name, info in self.products.items():
                tk.Label(self.root, text=f"{name}: ₹{info['price']:.2f} | Qty: {info['qty']}", font=("Arial", 14)).pack(anchor='w', padx=20)
        tk.Button(self.root, text="🔙 Back", font=("Arial", 12), command=self.main_menu).pack(pady=20)

    def low_stock_alert(self):
        self.clear_window()
        tk.Label(self.root, text="⚠️ Low Stock Products (Qty ≤ 5)", font=("Arial", 16, "bold")).pack(pady=15)
        low_stock = [ (n, i) for n, i in self.products.items() if i['qty'] <= 5]
        if not low_stock:
            tk.Label(self.root, text="✅ No low stock products.", font=("Arial", 14)).pack(pady=10)
        else:
            for name, info in low_stock:
                tk.Label(self.root, text=f"{name}: Qty {info['qty']}", font=("Arial", 14), fg="red").pack(anchor='w', padx=20)
        tk.Button(self.root, text="🔙 Back", font=("Arial", 12), command=self.main_menu).pack(pady=20)

    def simulate_sale(self):
        if not self.products:
            messagebox.showinfo("📭 Empty", "No products to sell.")
            return
        name = simpledialog.askstring("💰 Simulate Sale", "Enter product name:")
        if name not in self.products:
            messagebox.showerror("❌ Error", "Product not found!")
            return
        try:
            qty = int(simpledialog.askstring("Quantity", "Enter quantity to sell:"))
            if qty <= 0:
                raise ValueError
        except:
            messagebox.showerror("❌ Error", "Invalid quantity!")
            return
        if self.products[name]["qty"] < qty:
            messagebox.showerror("❌ Error", "Not enough stock!")
            return
        self.products[name]["qty"] -= qty
        total_price = qty * self.products[name]["price"]
        messagebox.showinfo("✅ Sale Complete", f"Sold {qty} x {name}\nTotal: ₹{total_price:.2f}")

    def logout(self):
        self.logged_user = None
        messagebox.showinfo("👋 Logout", "You have logged out.")
        self.login_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySystem(root)
    root.mainloop()
