import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from invoice_loader import InvoiceLoader
from fraud_model import process_fraud_check

TEST_JSON_FILE = "data/test_invoices.json"
PROCESSED_CSV_FILE = "processed_fraud_results.csv"


def process_new_file():
    """Loads and processes a new CSV file, converting it to JSON."""
    loader = InvoiceLoader()
    invoices = loader.load_invoices()
    if invoices:
        loader.save_to_json(invoices)
        messagebox.showinfo("Success", f"✅ File processed! Saved as {TEST_JSON_FILE}")
    else:
        messagebox.showerror("Error", "❌ No invoices found or failed to process CSV.")


def apply_flags():
    """Runs fraud detection on the processed JSON and outputs results as CSV."""
    if not os.path.exists(TEST_JSON_FILE):
        messagebox.showerror("Error", "❌ No JSON file found! Please process a CSV first.")
        return

    process_fraud_check(TEST_JSON_FILE)
    messagebox.showinfo("Success", f"✅ Fraud check completed! Saved as {PROCESSED_CSV_FILE}")


def exit_program():
    """Exits the application."""
    root.destroy()


# Create UI
root = tk.Tk()
root.title("Fraud Detection System")
root.geometry("400x300")

label = tk.Label(root, text="Choose an action:", font=("Arial", 12))
label.pack(pady=20)

btn_process = tk.Button(root, text="1️⃣ Process New File (CSV → JSON)", command=process_new_file)
btn_process.pack(pady=10)

btn_apply = tk.Button(root, text="2️⃣ Apply Flags (JSON → CSV)", command=apply_flags)
btn_apply.pack(pady=10)

btn_exit = tk.Button(root, text="❌ Exit", command=exit_program)
btn_exit.pack(pady=20)

root.mainloop()
