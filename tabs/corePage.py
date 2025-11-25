import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import tabs.networking as networking
import tabs.hashes as hashes
import tabs.behaviour as behaviour


def corePage(root):
    notebook = ttk.Notebook(root)
    notebook.grid(column=0, row=1, padx=10, pady=5, columnspan=2, sticky='nsew')

    general_frame = ttk.Frame(notebook)
    network_frame = ttk.Frame(notebook)
    hashes_frame = ttk.Frame(notebook)
    behaviour_frame = ttk.Frame(notebook)

    notebook.add(general_frame, text="General")
    notebook.add(network_frame, text="Networking")
    notebook.add(hashes_frame, text="Hashes")
    notebook.add(behaviour_frame, text="Behavior")

    tk.Label(general_frame, text="Rule ID:", font=("Arial", 12)).grid(column=0, row=0, sticky="w", padx=5, pady=2)
    id_entry = tk.Entry(general_frame, width=30)
    id_entry.grid(column=1, row=0, padx=5, pady=2)
    # Default Rule ID
    id_entry.insert(0, "100001")

    tk.Label(general_frame, text="Level:", font=("Arial", 12)).grid(column=0, row=1, sticky="w", padx=5, pady=2)
    level_entry = tk.Entry(general_frame, width=30)
    level_entry.grid(column=1, row=1, padx=5, pady=2)

    tk.Label(general_frame, text="Program Name:", font=("Arial", 12)).grid(column=0, row=2, sticky="w", padx=5, pady=2)
    name_entry = tk.Entry(general_frame, width=30)
    name_entry.grid(column=1, row=2, padx=5, pady=2)

    tk.Label(general_frame, text="Description:", font=("Arial", 12)).grid(column=0, row=3, sticky="w", padx=5, pady=2)
    description_entry = tk.Entry(general_frame, width=30)
    description_entry.grid(column=1, row=3, padx=5, pady=2)

    tk.Label(general_frame, text="Mitre:", font=("Arial", 12)).grid(column=0, row=4, sticky="w", padx=5, pady=2)
    mitre_entry = tk.Entry(general_frame, width=30)
    mitre_entry.grid(column=1, row=4, padx=5, pady=2)

    net_widgets = networking.populate(network_frame)
    hashes_widgets = hashes.populate(hashes_frame)
    behaviour_widgets = behaviour.populate(behaviour_frame)

    def get_values():
        vals = {}
        vals['id'] = id_entry.get().strip()
        vals['level'] = level_entry.get().strip()
        vals['program_name'] = name_entry.get().strip()
        vals['description'] = description_entry.get().strip()
        vals['mitre'] = mitre_entry.get().strip()

        # Networking
        vals['protocol'] = net_widgets['protocol'].get().strip()
        vals['src_ip'] = net_widgets['src_ip'].get().strip()
        vals['dst_ip'] = net_widgets['dst_ip'].get().strip()
        vals['port'] = net_widgets['port'].get().strip()
        # New networking fields
        vals['domain'] = net_widgets.get('domain').get().strip()
        vals['http_path'] = net_widgets.get('http_path').get().strip()
        vals['http_method'] = net_widgets.get('http_method').get().strip()
        vals['user_agent'] = net_widgets.get('user_agent').get().strip()

        # Hashes
        # Combobox and entries both support .get()
        vals['hash_type'] = hashes_widgets['hash_type'].get().strip()
        vals['hash_value'] = hashes_widgets['hash_value'].get().strip()
        vals['file_path'] = hashes_widgets['file_path'].get().strip()

        # Behaviour
        vals['behavior_type'] = behaviour_widgets['behavior_type'].get().strip()
        vals['process_name'] = behaviour_widgets['process_name'].get().strip()
        vals['command_line'] = behaviour_widgets['command_line'].get().strip()

        return vals

    def reset_fields():
        # Reset general fields
        try:
            id_entry.delete(0, 'end')
            id_entry.insert(0, '100001')
        except Exception:
            pass
        try:
            level_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            name_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            description_entry.delete(0, 'end')
        except Exception:
            pass
        try:
            mitre_entry.delete(0, 'end')
        except Exception:
            pass

        # Networking widgets
        for w in net_widgets.values():
            try:
                if hasattr(w, 'set'):
                    w.set('')
                elif hasattr(w, 'delete'):
                    w.delete(0, 'end')
            except Exception:
                pass

        # Hashes widgets
        for w in hashes_widgets.values():
            try:
                if hasattr(w, 'set'):
                    w.set('')
                elif hasattr(w, 'delete'):
                    w.delete(0, 'end')
            except Exception:
                pass

        # Behaviour widgets
        for w in behaviour_widgets.values():
            try:
                if hasattr(w, 'set'):
                    w.set('')
                elif hasattr(w, 'delete'):
                    w.delete(0, 'end')
            except Exception:
                pass

    return get_values, reset_fields