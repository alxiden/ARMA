import tkinter as tk
from tkinter import ttk

def populate(frame):
    tk.Label(frame, text="Protocol:", font=("Arial", 12)).grid(column=0, row=0, sticky="w", padx=5, pady=2)
    proto_entry = tk.Entry(frame, width=30)
    proto_entry.grid(column=1, row=0, padx=5, pady=2)

    tk.Label(frame, text="Source IP:", font=("Arial", 12)).grid(column=0, row=1, sticky="w", padx=5, pady=2)
    src_entry = tk.Entry(frame, width=30)
    src_entry.grid(column=1, row=1, padx=5, pady=2)

    tk.Label(frame, text="Destination IP:", font=("Arial", 12)).grid(column=0, row=2, sticky="w", padx=5, pady=2)
    dst_entry = tk.Entry(frame, width=30)
    dst_entry.grid(column=1, row=2, padx=5, pady=2)

    tk.Label(frame, text="Port:", font=("Arial", 12)).grid(column=0, row=3, sticky="w", padx=5, pady=2)
    port_entry = tk.Entry(frame, width=30)
    port_entry.grid(column=1, row=3, padx=5, pady=2)
    # Return references so caller can read values
    return {
        'protocol': proto_entry,
        'src_ip': src_entry,
        'dst_ip': dst_entry,
        'port': port_entry,
    }
