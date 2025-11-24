import tkinter as tk
from tkinter import messagebox
import tabs.corePage as corePage
import rule_builder
import validator


def app():
    root = tk.Tk()
    root.title("ARMA Application")
    root.geometry("400x400")

    title = tk.Label(root, text="Welcome to the ARMA Application!", font=("Arial", 16))
    title.grid(column=0, row=0, padx=20, pady=20, columnspan=2)

    gather = corePage.corePage(root)

    # Rule generation was moved to `rule_builder.build_wazuh_rule`

    def show_rule_popup(text: str):
        popup = tk.Toplevel(root)
        popup.title("Generated Wazuh Rule")
        popup.geometry("700x400")

        tk.Label(popup, text="Copy the XML below into your Wazuh rules file:", font=("Arial", 11)).pack(padx=8, pady=8, anchor='w')

        txt = tk.Text(popup, wrap='none')
        txt.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        txt.insert('1.0', text)
        txt.config(state='normal')

        def copy_to_clipboard():
            root.clipboard_clear()
            root.clipboard_append(text)
            messagebox.showinfo("Copied", "Rule copied to clipboard")

        btn_frame = tk.Frame(popup)
        btn_frame.pack(fill='x', padx=8, pady=6)
        tk.Button(btn_frame, text="Copy to clipboard", command=copy_to_clipboard).pack(side='left')
        tk.Button(btn_frame, text="Close", command=popup.destroy).pack(side='right')

    def on_create():
        vals = gather()
        valid, errors = validator.validate_all(vals)
        if not valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        rule_xml = rule_builder.build_wazuh_rule(vals)
        show_rule_popup(rule_xml)

    create_button = tk.Button(root, text="Create Rule", font=("Arial", 12), command=on_create)
    create_button.grid(column=0, row=5, columnspan=2, pady=20)

    root.mainloop()


if __name__ == "__main__":
    app()