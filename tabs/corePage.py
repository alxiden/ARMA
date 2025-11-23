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
    
    # SIEM selection checkboxes
    tk.Label(general_frame, text="Target SIEMs:", font=("Arial", 12)).grid(column=0, row=5, sticky="w", padx=5, pady=6)
    siem_frame = ttk.Frame(general_frame)
    siem_frame.grid(column=1, row=5, sticky='w', padx=5, pady=6)
    wazuh_var = tk.BooleanVar(value=True)
    elastic_var = tk.BooleanVar(value=False)
    splunk_var = tk.BooleanVar(value=False)
    tk.Checkbutton(siem_frame, text='Wazuh', variable=wazuh_var).pack(side='left')
    tk.Checkbutton(siem_frame, text='Elastic', variable=elastic_var).pack(side='left')
    tk.Checkbutton(siem_frame, text='Splunk', variable=splunk_var).pack(side='left')

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
        vals['siem_wazuh'] = bool(wazuh_var.get())
        vals['siem_elastic'] = bool(elastic_var.get())
        vals['siem_splunk'] = bool(splunk_var.get())

        # Networking
        vals['protocol'] = net_widgets['protocol'].get().strip()
        vals['src_ip'] = net_widgets['src_ip'].get().strip()
        vals['dst_ip'] = net_widgets['dst_ip'].get().strip()
        vals['port'] = net_widgets['port'].get().strip()

        # Hashes
        # Combobox and entries both support .get()
        vals['hash_type'] = hashes_widgets['hash_type'].get().strip()
        vals['hash_value'] = hashes_widgets['hash_value'].get().strip()
        vals['file_path'] = hashes_widgets['file_path'].get().strip()

        # Behaviour
        vals['behavior_type'] = behaviour_widgets['behavior_type'].get().strip()
        vals['process_name'] = behaviour_widgets['process_name'].get().strip()
        vals['command_line'] = behaviour_widgets['command_line'].get().strip()
        # persistence is BooleanVar
        vals['persistence'] = bool(behaviour_widgets['persistence'].get())

        return vals

    return get_values