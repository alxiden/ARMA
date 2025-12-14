import tkinter as tk
from tkinter import ttk


def populate(frame):
    rows = []

    header_font = ("Arial", 10, "bold")
    tk.Label(frame, text="Identifier", font=header_font).grid(column=0, row=0, padx=5, pady=(5, 2), sticky="w")
    tk.Label(frame, text="Type", font=header_font).grid(column=1, row=0, padx=5, pady=(5, 2), sticky="w")
    tk.Label(frame, text="Value", font=header_font).grid(column=2, row=0, padx=5, pady=(5, 2), sticky="w")

    for i in range(5):
        ident = tk.Entry(frame, width=18)
        ident.grid(column=0, row=i + 1, padx=5, pady=2, sticky="w")

        stype = ttk.Combobox(frame, values=["text", "regex", "hex"], width=10, state="readonly")
        stype.grid(column=1, row=i + 1, padx=5, pady=2, sticky="w")

        value = tk.Entry(frame, width=40)
        value.grid(column=2, row=i + 1, padx=5, pady=2, sticky="we")

        rows.append({"id": ident, "type": stype, "value": value})

    frame.columnconfigure(2, weight=1)
    return rows
