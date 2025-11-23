import tkinter as tk
from tkinter import ttk

def populate(frame):
    tk.Label(frame, text="Hash Type:", font=("Arial", 12)).grid(column=0, row=0, sticky="w", padx=5, pady=2)
    hash_type = ttk.Combobox(frame, values=["MD5", "SHA1", "SHA256"], width=28)
    hash_type.grid(column=1, row=0, padx=5, pady=2)

    tk.Label(frame, text="Hash Value:", font=("Arial", 12)).grid(column=0, row=1, sticky="w", padx=5, pady=2)
    hash_entry = tk.Entry(frame, width=30)
    hash_entry.grid(column=1, row=1, padx=5, pady=2)

    tk.Label(frame, text="File Path:", font=("Arial", 12)).grid(column=0, row=2, sticky="w", padx=5, pady=2)
    file_entry = tk.Entry(frame, width=30)
    file_entry.grid(column=1, row=2, padx=5, pady=2)
    # Return references so caller can read values
    return {
        'hash_type': hash_type,
        'hash_value': hash_entry,
        'file_path': file_entry,
    }
