import tkinter as tk
from tkinter import ttk

def populate(frame):
    tk.Label(frame, text="Behavior Type:", font=("Arial", 12)).grid(column=0, row=0, sticky="w", padx=5, pady=2)
    btype_entry = tk.Entry(frame, width=30)
    btype_entry.grid(column=1, row=0, padx=5, pady=2)

    tk.Label(frame, text="Process Name:", font=("Arial", 12)).grid(column=0, row=1, sticky="w", padx=5, pady=2)
    proc_entry = tk.Entry(frame, width=30)
    proc_entry.grid(column=1, row=1, padx=5, pady=2)

    tk.Label(frame, text="Command Line:", font=("Arial", 12)).grid(column=0, row=2, sticky="w", padx=5, pady=2)
    cmd_entry = tk.Entry(frame, width=30)
    cmd_entry.grid(column=1, row=2, padx=5, pady=2)

    tk.Label(frame, text="Persistence:", font=("Arial", 12)).grid(column=0, row=3, sticky="w", padx=5, pady=2)
    persistence_var = tk.BooleanVar()
    tk.Checkbutton(frame, variable=persistence_var).grid(column=1, row=3, sticky="w", padx=5, pady=2)
    # Return references (note: persistence is a BooleanVar)
    return {
        'behavior_type': btype_entry,
        'process_name': proc_entry,
        'command_line': cmd_entry,
        'persistence': persistence_var,
    }
