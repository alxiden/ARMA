import tkinter as tk
from tkinter import ttk

import tabs.strings as strings


def corePage(root):
    notebook = ttk.Notebook(root)
    notebook.grid(column=0, row=1, padx=10, pady=5, columnspan=2, sticky='nsew')

    general_frame = ttk.Frame(notebook)
    strings_frame = ttk.Frame(notebook)

    notebook.add(general_frame, text="General")
    notebook.add(strings_frame, text="Strings")

    tk.Label(general_frame, text="Rule Name:", font=("Arial", 12)).grid(column=0, row=0, sticky="w", padx=5, pady=2)
    name_entry = tk.Entry(general_frame, width=30)
    name_entry.grid(column=1, row=0, padx=5, pady=2)

    tk.Label(general_frame, text="Tags (space or comma separated):", font=("Arial", 12)).grid(column=0, row=1, sticky="w", padx=5, pady=2)
    tags_entry = tk.Entry(general_frame, width=30)
    tags_entry.grid(column=1, row=1, padx=5, pady=2)

    tk.Label(general_frame, text="Author:", font=("Arial", 12)).grid(column=0, row=2, sticky="w", padx=5, pady=2)
    author_entry = tk.Entry(general_frame, width=30)
    author_entry.grid(column=1, row=2, padx=5, pady=2)

    tk.Label(general_frame, text="Description:", font=("Arial", 12)).grid(column=0, row=3, sticky="w", padx=5, pady=2)
    description_entry = tk.Entry(general_frame, width=30)
    description_entry.grid(column=1, row=3, padx=5, pady=2)

    tk.Label(general_frame, text="Reference/Link:", font=("Arial", 12)).grid(column=0, row=4, sticky="w", padx=5, pady=2)
    reference_entry = tk.Entry(general_frame, width=30)
    reference_entry.grid(column=1, row=4, padx=5, pady=2)

    tk.Label(general_frame, text="Condition:", font=("Arial", 12)).grid(column=0, row=5, sticky="nw", padx=5, pady=2)
    condition_entry = tk.Text(general_frame, width=30, height=3)
    condition_entry.grid(column=1, row=5, padx=5, pady=2, sticky='we')
    condition_entry.insert('1.0', 'any of them')

    string_rows = strings.populate(strings_frame)

    def get_values():
        vals = {}
        vals['rule_name'] = name_entry.get().strip()
        vals['tags'] = tags_entry.get().strip()
        vals['author'] = author_entry.get().strip()
        vals['description'] = description_entry.get().strip()
        vals['reference'] = reference_entry.get().strip()
        condition_text = condition_entry.get('1.0', 'end').strip()
        vals['condition'] = condition_text or 'any of them'

        strings_vals = []
        for row in string_rows:
            sid = row['id'].get().strip()
            stype = (row['type'].get() or '').strip()
            sval = row['value'].get().strip()
            if not sid and not sval and not stype:
                continue
            strings_vals.append({'id': sid, 'type': stype or 'text', 'value': sval})

        vals['strings'] = strings_vals
        return vals

    def reset_fields():
        try:
            name_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            tags_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            author_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            description_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            reference_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            condition_entry.delete('1.0', 'end')
            condition_entry.insert('1.0', 'any of them')
        except Exception:
            pass

        for row in string_rows:
            for widget in row.values():
                try:
                    if hasattr(widget, 'set'):
                        widget.set('')
                    elif hasattr(widget, 'delete'):
                        widget.delete(0, 'end')
                except Exception:
                    pass

    return get_values, reset_fields