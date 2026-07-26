import tkinter as tk
from tkinter import messagebox
import random


class BillApp:
    # Single source of truth for items & prices: category -> [(name, price), ...]
    ITEMS = {
        "Cosmetics": [("Bath Soap", 2), ("Face Cream", 5), ("Shampoo", 4)],
        "Grocery": [("Rice", 10), ("Food Oil", 7), ("Sugar", 3)],
        "Cold Drinks": [("Coke", 2), ("Sprite", 2), ("Water", 1)],
    }

    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700")
        self.root.title("Bill Management System")
        self.root.configure(bg="#2c3e50")

        # ================= Variables =================
        # Customer Info
        self.c_name = tk.StringVar()
        self.c_phone = tk.StringVar()
        self.bill_no = tk.StringVar()
        self.bill_no.set(str(random.randint(1000, 9999)))

        # Quantities: item name -> StringVar (digit-only, validated on keystroke)
        self.quantities = {}
        for entries in self.ITEMS.values():
            for name, _price in entries:
                self.quantities[name] = tk.StringVar(value="0")

        # Category + grand totals
        self.category_totals = {category: tk.StringVar(value="R0") for category in self.ITEMS}
        self.grand_total = tk.StringVar(value="R0")
        self.total_bill = 0

        # Registered validator for quantity entries: digits only, empty allowed while typing
        self.vcmd = (self.root.register(self._validate_qty), "%P")

        # ================= UI Design =================
        title = tk.Label(self.root, text="Billing Management System", bd=12, relief=tk.GROOVE,
                          bg="#1abc9c", fg="white", font=("times new roman", 24, "bold"), pady=2)
        title.pack(fill=tk.X)

        # Customer Details Frame
        F1 = tk.LabelFrame(self.root, text="Customer Details", font=("times new roman", 12, "bold"), fg="gold", bg="#2c3e50")
        F1.pack(fill=tk.X, pady=5, padx=10)

        tk.Label(F1, text="Customer Name:", bg="#2c3e50", fg="white", font=("times new roman", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(F1, width=20, textvariable=self.c_name, font="arial 12").grid(row=0, column=1, padx=10, pady=5)

        tk.Label(F1, text="Phone No:", bg="#2c3e50", fg="white", font=("times new roman", 12, "bold")).grid(row=0, column=2, padx=10, pady=5)
        tk.Entry(F1, width=20, textvariable=self.c_phone, font="arial 12").grid(row=0, column=3, padx=10, pady=5)

        tk.Label(F1, text="Bill No:", bg="#2c3e50", fg="white", font=("times new roman", 12, "bold")).grid(row=0, column=4, padx=10, pady=5)
        tk.Entry(F1, width=15, textvariable=self.bill_no, font="arial 12", state="readonly").grid(row=0, column=5, padx=10, pady=5)

        # Main Content Frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # One category frame per entry in ITEMS, built from the data instead of copy-pasted
        for category, entries in self.ITEMS.items():
            frame = tk.LabelFrame(main_frame, text=category, font=("times new roman", 12, "bold"), fg="gold", bg="#2c3e50")
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            for row, (name, price) in enumerate(entries):
                self.create_item(frame, name, price, row)

        # Bill Area Frame
        F5 = tk.Frame(main_frame, bd=4, relief=tk.GROOVE)
        F5.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(F5, text="Bill Area", font="arial 12 bold", bd=5, relief=tk.GROOVE).pack(fill=tk.X)

        # Summary panel: category totals + grand total actually displayed now
        summary = tk.Frame(F5, bg="#ecf0f1")
        summary.pack(fill=tk.X)
        for category in self.ITEMS:
            row = tk.Frame(summary, bg="#ecf0f1")
            row.pack(fill=tk.X, padx=8, pady=2)
            tk.Label(row, text=f"{category}:", bg="#ecf0f1", font=("arial", 10, "bold"), anchor="w").pack(side=tk.LEFT)
            tk.Label(row, textvariable=self.category_totals[category], bg="#ecf0f1", font=("arial", 10)).pack(side=tk.RIGHT)
        grand_row = tk.Frame(summary, bg="#ecf0f1")
        grand_row.pack(fill=tk.X, padx=8, pady=(2, 6))
        tk.Label(grand_row, text="Grand Total:", bg="#ecf0f1", font=("arial", 11, "bold"), anchor="w").pack(side=tk.LEFT)
        tk.Label(grand_row, textvariable=self.grand_total, bg="#ecf0f1", font=("arial", 11, "bold")).pack(side=tk.RIGHT)

        scroll_y = tk.Scrollbar(F5, orient=tk.VERTICAL)
        self.textarea = tk.Text(F5, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=tk.BOTH, expand=True)

        # Button Menu Frame
        F6 = tk.LabelFrame(self.root, text="Billing Menu", font=("times new roman", 12, "bold"), fg="gold", bg="#2c3e50")
        F6.pack(fill=tk.X, pady=5, padx=10)

        btn_frame = tk.Frame(F6, bg="#2c3e50")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Total", command=self.calculate_total, bg="#3498db", fg="white", font=("arial", 12, "bold"), width=12).grid(row=0, column=0, padx=15)
        tk.Button(btn_frame, text="Generate Bill", command=self.generate_bill, bg="#2ecc71", fg="white", font=("arial", 12, "bold"), width=12).grid(row=0, column=1, padx=15)
        tk.Button(btn_frame, text="Clear", command=self.clear_data, bg="#e67e22", fg="white", font=("arial", 12, "bold"), width=12).grid(row=0, column=2, padx=15)
        tk.Button(btn_frame, text="Exit", command=self.exit_app, bg="#e74c3c", fg="white", font=("arial", 12, "bold"), width=12).grid(row=0, column=3, padx=15)

        self.welcome_bill()

    # ================= Helper Methods =================
    def create_item(self, frame, name, price, row_num):
        """Creates an item label and a validated quantity entry."""
        tk.Label(frame, text=f"{name} (R{price})", font=("times new roman", 12, "bold"), bg="#2c3e50", fg="lightgreen").grid(row=row_num, column=0, pady=10, padx=10, sticky="w")
        tk.Entry(frame, width=8, textvariable=self.quantities[name], font="arial 12",
                  validate="key", validatecommand=self.vcmd).grid(row=row_num, column=1, pady=10, padx=10)

    def _validate_qty(self, proposed_value):
        """Entry-level validator: only digits allowed (blocks letters, minus signs,
        and anything else that would make IntVar-style parsing crash). Empty string
        is allowed so the user can clear the box while typing; it's treated as 0
        everywhere else."""
        return proposed_value == "" or proposed_value.isdigit()

    def get_qty(self, name):
        """Safely reads a quantity, treating blank/invalid entries as 0 instead of
        raising (this replaces the old IntVar.get() calls that crashed on empty
        fields)."""
        value = self.quantities[name].get()
        return int(value) if value.isdigit() else 0

    # ================= Logic Methods =================
    def calculate_total(self, show_message=True):
        """Calculates totals per category and overall, driven by self.ITEMS so
        prices only ever live in one place."""
        grand_total = 0
        for category, entries in self.ITEMS.items():
            cat_total = sum(self.get_qty(name) * price for name, price in entries)
            self.category_totals[category].set(f"R{cat_total}")
            grand_total += cat_total

        self.grand_total.set(f"R{grand_total}")
        self.total_bill = grand_total

        if show_message:
            messagebox.showinfo("Success", f"Totals calculated. Grand Total: R{grand_total}")

        return grand_total

    def welcome_bill(self):
        """Generates the header for the receipt."""
        self.textarea.delete('1.0', tk.END)
        self.textarea.insert(tk.END, "\tWelcome to Super Retail\n")
        self.textarea.insert(tk.END, f"\nBill Number: {self.bill_no.get()}")
        self.textarea.insert(tk.END, f"\nCustomer Name: {self.c_name.get()}")
        self.textarea.insert(tk.END, f"\nPhone Number: {self.c_phone.get()}")
        self.textarea.insert(tk.END, "\n======================================")
        self.textarea.insert(tk.END, "\nProduct\t\tQty\t\tPrice")
        self.textarea.insert(tk.END, "\n======================================")

    def generate_bill(self):
        """Formats the items into the receipt text area."""
        if self.c_name.get() == "" or self.c_phone.get() == "":
            messagebox.showerror("Error", "Customer details are required")
            return

        # show_message=False: avoids popping up the "Totals calculated" dialog
        # on top of the receipt itself
        total = self.calculate_total(show_message=False)

        if total == 0:
            messagebox.showerror("Error", "No items selected to bill")
            return

        self.welcome_bill()

        for entries in self.ITEMS.values():
            for name, price in entries:
                qty = self.get_qty(name)
                if qty != 0:
                    self.textarea.insert(tk.END, f"\n{name}\t\t{qty}\t\tR{qty * price}")

        self.textarea.insert(tk.END, "\n======================================")
        self.textarea.insert(tk.END, f"\nTotal Bill:\t\t\tR{total}")
        self.textarea.insert(tk.END, "\n======================================")

    def clear_data(self):
        """Resets all fields and variables."""
        self.c_name.set("")
        self.c_phone.set("")
        self.bill_no.set(str(random.randint(1000, 9999)))

        for var in self.quantities.values():
            var.set("0")

        for category in self.category_totals:
            self.category_totals[category].set("R0")
        self.grand_total.set("R0")
        self.total_bill = 0

        self.welcome_bill()

    def exit_app(self):
        """Safely closes the application."""
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BillApp(root)
    root.mainloop()