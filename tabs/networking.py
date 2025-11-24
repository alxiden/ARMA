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
    
    # New: Domain and HTTP request fields
    tk.Label(frame, text="Domain:", font=("Arial", 12)).grid(column=0, row=4, sticky="w", padx=5, pady=2)
    domain_entry = tk.Entry(frame, width=30)
    domain_entry.grid(column=1, row=4, padx=5, pady=2)

    tk.Label(frame, text="HTTP Path/URL:", font=("Arial", 12)).grid(column=0, row=5, sticky="w", padx=5, pady=2)
    http_path_entry = tk.Entry(frame, width=30)
    http_path_entry.grid(column=1, row=5, padx=5, pady=2)

    tk.Label(frame, text="HTTP Method:", font=("Arial", 12)).grid(column=0, row=6, sticky="w", padx=5, pady=2)
    http_method = ttk.Combobox(frame, values=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"], width=28)
    http_method.grid(column=1, row=6, padx=5, pady=2)

    tk.Label(frame, text="User-Agent:", font=("Arial", 12)).grid(column=0, row=7, sticky="w", padx=5, pady=2)
    ua_entry = tk.Entry(frame, width=30)
    ua_entry.grid(column=1, row=7, padx=5, pady=2)
    # Return references so caller can read values
    return {
        'protocol': proto_entry,
        'src_ip': src_entry,
        'dst_ip': dst_entry,
        'port': port_entry,
        'domain': domain_entry,
        'http_path': http_path_entry,
        'http_method': http_method,
        'user_agent': ua_entry,
    }
