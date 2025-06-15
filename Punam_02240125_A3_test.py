import unittest
from Punam_02240125_A3_PA import BankAccount, InvalidAmountError, InsufficientFundsError

# test_Punam_02240125_A3_PA.py


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc1 = BankAccount("12345", "Alice", "1234", 1000)
        self.acc2 = BankAccount("54321", "Bob", "4321", 500)

    def test_deposit_positive(self):
        self.acc1.deposit(200)
        self.assertEqual(self.acc1.balance, 1200)
        self.assertIn("Deposited Nu.200.00", self.acc1.get_transactions()[-1])

    def test_deposit_zero(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.deposit(0)

    def test_deposit_negative(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.deposit(-50)

    def test_withdraw_valid(self):
        self.acc1.withdraw(300)
        self.assertEqual(self.acc1.balance, 700)
        self.assertIn("Withdrew Nu.300.00", self.acc1.get_transactions()[-1])

    def test_withdraw_zero(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.withdraw(0)

    def test_withdraw_negative(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.withdraw(-10)

    def test_withdraw_over_balance(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc1.withdraw(2000)

    def test_transfer_valid(self):
        self.acc1.transfer(400, self.acc2)
        self.assertEqual(self.acc1.balance, 600)
        self.assertEqual(self.acc2.balance, 900)
        self.assertIn("Sent Nu.400.00 to Bob", self.acc1.get_transactions()[-1])
        self.assertIn("Received Nu.400.00 from Alice", self.acc2.get_transactions()[-1])

    def test_transfer_to_self(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.transfer(100, self.acc1)

    def test_transfer_negative(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.transfer(-50, self.acc2)

    def test_transfer_over_balance(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc1.transfer(2000, self.acc2)

    def test_mobile_topup_valid(self):
        self.acc1.mobile_topup(100, "17123456")
        self.assertEqual(self.acc1.balance, 900)
        self.assertIn("Mobile top-up Nu.100.00 to 17123456", self.acc1.get_transactions()[-1])

    def test_mobile_topup_negative(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.mobile_topup(-20, "17123456")

    def test_mobile_topup_over_balance(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc1.mobile_topup(2000, "17123456")

    def test_transaction_history(self):
        self.acc1.deposit(100)
        self.acc1.withdraw(50)
        self.acc1.mobile_topup(20, "17123456")
        txns = self.acc1.get_transactions()
        self.assertEqual(len(txns), 3)
        self.assertIn("Deposited Nu.100.00", txns[0])
        self.assertIn("Withdrew Nu.50.00", txns[1])
        self.assertIn("Mobile top-up Nu.20.00 to 17123456", txns[2])

if __name__ == "__main__":
    unittest.main()