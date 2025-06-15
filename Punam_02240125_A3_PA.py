import tkinter as tk
from tkinter import messagebox, simpledialog
import random


class InvalidAmountError(Exception):
    """Exception raised for invalid monetary amounts."""
    pass


class InsufficientFundsError(Exception):
    """Exception raised when account has insufficient funds."""
    pass


class BankAccount:
    """A class representing a bank account with basic banking operations."""

    def __init__(self, account_number, name, passcode, balance=0):
        """Initialize a BankAccount with basic account information."""
        self.account_number = account_number
        self.name = name
        self.passcode = passcode
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        self.balance += amount
        self.transactions.append(f"Deposited Nu.{amount:.2f}")

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Withdrew Nu.{amount:.2f}")

    def transfer(self, amount, target):
        """Transfer money to another account."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        if target == self:
            raise InvalidAmountError("Cannot transfer to same account")
        self.balance -= amount
        target.balance += amount
        self.transactions.append(f"Sent Nu.{amount:.2f} to {target.name}")
        target.transactions.append(f"Received Nu.{amount:.2f} from {self.name}")

    def mobile_topup(self, amount, number):
        """Perform mobile phone credit top-up."""
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Mobile top-up Nu.{amount:.2f} to {number}")

    def get_transactions(self):
        """Get the transaction history for this account."""
        return self.transactions


class PFinanceApp:
    """A GUI application for P Finance banking operations."""

    def __init__(self, master):
        """Initialize the P Finance application GUI."""
        self.master = master
        master.title("P Finance - Digital Banking")
        master.geometry("500x600")
        
        # Modern color scheme
        self.bg_color = "#f0f8ff"
        self.primary_color = "#2e5cb8"
        self.secondary_color = "#ff6600"
        
        master.configure(bg=self.bg_color)
        
        # Main header
        header = tk.Frame(master, bg=self.primary_color)
        header.pack(fill=tk.X)
        tk.Label(header, text="P Finance", font=("Helvetica", 20, "bold"), 
                fg="white", bg=self.primary_color).pack(pady=10)
        
        # Account controls
        control_frame = tk.Frame(master, bg=self.bg_color)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Open Account", command=self.open_account,
                 bg=self.secondary_color, fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Login", command=self.login,
                 bg=self.secondary_color, fg="white").pack(side=tk.LEFT, padx=5)
        
        # Transaction buttons (initially disabled)
        self.transaction_frame = tk.Frame(master, bg=self.bg_color)
        self.transaction_frame.pack(pady=10)
        
        buttons = [
            ("Deposit", self.deposit),
            ("Withdraw", self.withdraw),
            ("Send Money", self.transfer),
            ("Mobile Top-Up", self.mobile_topup),
            ("Close Account", self.close_account)
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.transaction_frame, text=text, command=command,
                           state=tk.DISABLED, bg=self.primary_color, fg="white")
            btn.pack(fill=tk.X, pady=2)
        
        # Account info display
        self.info_frame = tk.Frame(master, bg=self.bg_color)
        self.info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.balance_label = tk.Label(self.info_frame, text="No account selected", 
                                    font=("Helvetica", 12), bg=self.bg_color)
        self.balance_label.pack()
        
        # Transaction history
        txn_frame = tk.LabelFrame(master, text="Transaction History", bg=self.bg_color)
        txn_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.txn_text = tk.Text(txn_frame, height=10, state=tk.DISABLED)
        self.txn_text.pack(fill=tk.BOTH, expand=True)
        
        # Logout button
        tk.Button(master, text="Logout", command=self.logout,
                 bg="#666666", fg="white").pack(side=tk.BOTTOM, pady=10)
        
        self.accounts = {}
        self.current = None

    def generate_account_number(self):
        """Generate a unique 5-digit account number."""
        while True:
            acc_num = str(random.randint(10000, 99999))
            if acc_num not in self.accounts:
                return acc_num

    def open_account(self):
        """Open a new bank account through a dialog interface."""
        name = simpledialog.askstring("Open Account", "Enter account holder name:")
        if not name:
            return
            
        # Check for duplicate names
        for acc in self.accounts.values():
            if acc.name == name:
                messagebox.showerror("Error", "Account with this name already exists")
                return
                
        passcode = simpledialog.askstring("Set Passcode", "Set a numeric passcode (min 4 digits):", show="*")
        if not passcode or not passcode.isdigit() or len(passcode) < 4:
            messagebox.showerror("Error", "Invalid passcode. Must be at least 4 digits.")
            return
            
        bal = simpledialog.askfloat("Open Account", "Enter opening balance (Nu.):", minvalue=500)
        if bal is not None:
            acc_num = self.generate_account_number()
            self.accounts[acc_num] = BankAccount(acc_num, name, passcode, bal)
            messagebox.showinfo("Success", 
                f"Account opened for {name}\nAccount Number: {acc_num}\nInitial Balance: Nu.{bal:.2f}")

    def login(self):
        """Authenticate user and log into an account."""
        if not self.accounts:
            messagebox.showerror("Error", "No accounts exist yet")
            return
            
        acc_num = simpledialog.askstring("Login", "Enter account number:")
        if acc_num in self.accounts:
            passcode = simpledialog.askstring("Passcode", "Enter your passcode:", show="*")
            if passcode != self.accounts[acc_num].passcode:
                messagebox.showerror("Error", "Incorrect passcode")
                return
                
            self.current = self.accounts[acc_num]
            self.update_display()
            # Enable transaction buttons
            for btn in self.transaction_frame.winfo_children():
                btn.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Account not found")

    def update_display(self):
        """Update the account information and transaction history display."""
        if self.current:
            self.balance_label.config(
                text=f"Account: {self.current.account_number}\n"
                     f"Holder: {self.current.name}\n"
                     f"Balance: Nu.{self.current.balance:.2f}")
            
            self.txn_text.config(state=tk.NORMAL)
            self.txn_text.delete(1.0, tk.END)
            
            if not self.current.transactions:
                self.txn_text.insert(tk.END, "No transactions yet")
            else:
                for t in reversed(self.current.transactions[-10:]):  # Show last 10 transactions
                    self.txn_text.insert(tk.END, f"• {t}\n")
                    
            self.txn_text.config(state=tk.DISABLED)

    def deposit(self):
        """Deposit money into current account through dialog."""
        amt = simpledialog.askfloat("Deposit", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.deposit(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Deposited Nu.{amt:.2f}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def withdraw(self):
        """Withdraw money from current account through dialog."""
        amt = simpledialog.askfloat("Withdraw", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.withdraw(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Withdrew Nu.{amt:.2f}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def transfer(self):
        """Transfer money to another account through dialog."""
        if len(self.accounts) < 2:
            messagebox.showerror("Error", "Need at least 2 accounts to transfer")
            return
            
        target_acc_num = simpledialog.askstring("Send Money", "Enter recipient account number:")
        if target_acc_num and target_acc_num in self.accounts and target_acc_num != self.current.account_number:
            amt = simpledialog.askfloat("Send Money", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try:
                    self.current.transfer(amt, self.accounts[target_acc_num])
                    self.update_display()
                    messagebox.showinfo("Success", 
                        f"Transferred Nu.{amt:.2f} to {self.accounts[target_acc_num].name}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Invalid recipient account")

    def mobile_topup(self):
        """Perform mobile phone credit top-up through dialog."""
        number = simpledialog.askstring("Mobile Top-Up", "Enter mobile number:")
        if number:
            amt = simpledialog.askfloat("Mobile Top-Up", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try:
                    self.current.mobile_topup(amt, number)
                    self.update_display()
                    messagebox.showinfo("Success", f"Topped up Nu.{amt:.2f} to {number}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def close_account(self):
        """Close the current account after confirmation."""
        if self.current:
            confirm = messagebox.askyesno("Close Account", 
                f"Close account for {self.current.name} ({self.current.account_number})?")
            if confirm:
                del self.accounts[self.current.account_number]
                self.current = None
                self.balance_label.config(text="No account selected")
                self.txn_text.config(state=tk.NORMAL)
                self.txn_text.delete(1.0, tk.END)
                self.txn_text.config(state=tk.DISABLED)
                # Disable transaction buttons
                for btn in self.transaction_frame.winfo_children():
                    btn.config(state=tk.DISABLED)
                messagebox.showinfo("Success", "Account closed successfully")

    def logout(self):
        """Log out of current account and reset the interface."""
        if self.current:
            self.current = None
            self.balance_label.config(text="No account selected")
            self.txn_text.config(state=tk.NORMAL)
            self.txn_text.delete(1.0, tk.END)
            self.txn_text.config(state=tk.DISABLED)
            # Disable transaction buttons
            for btn in self.transaction_frame.winfo_children():
                btn.config(state=tk.DISABLED)
            messagebox.showinfo("Logout", "You have been logged out.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PFinanceApp(root)
    root.mainloop()