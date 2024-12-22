import tkinter as tk
from tkinter import ttk
from . import CaesarCipher
from . import Playfair
from . import TranspositionMatrix


class Display:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cypher Wire")
        self.root.geometry("600x500")

        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, expand=True, fill="both")

        self.title_label = tk.Label(
            main_frame, text="Cypher Wire", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(main_frame, text="Enter Plaintext:").grid(
            row=1, column=0, padx=10, pady=10)
        self.input_plaintext = tk.Entry(main_frame, width=40)
        self.input_plaintext.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(main_frame, text="Enter Key:").grid(
            row=2, column=0, padx=10, pady=10)
        self.input_key = tk.Entry(main_frame, width=40)
        self.input_key.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(main_frame, text="Select Encryption Method:").grid(
            row=3, column=0, padx=10, pady=10)

        # Add Combobox for methods
        self.methods = {
            "Caesar cipher": CaesarCipher,
            "Playfair": Playfair,
            "TranspositionMatrix": TranspositionMatrix
        }
        self.method_var = tk.StringVar(value="Caesar cipher")
        self.method_selector = ttk.Combobox(
            main_frame, textvariable=self.method_var, values=list(self.methods.keys()), width=20)
        self.method_selector.grid(row=3, column=1, padx=(10, 0), pady=10, sticky="w")

        # Add Spinbox for additional parameter
        self.spinbox_var = tk.IntVar(value=1)  # Default value for Spinbox
        self.spinbox = ttk.Spinbox(
            main_frame, from_=1, to=10, textvariable=self.spinbox_var, width=5, increment=1)
        self.spinbox.grid(row=3, column=1, padx=(200, 0), pady=10, sticky="w")

        tk.Label(main_frame, text="Ciphertext:").grid(
            row=4, column=0, padx=10, pady=10)
        self.output_ciphertext = tk.Entry(main_frame, width=40)
        self.output_ciphertext.grid(row=4, column=1, padx=10, pady=10)

        self.error_label = tk.Label(main_frame, text="", fg="red")
        self.error_label.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(main_frame, text="Clear", command=self.clear_entries).grid(
            row=6, column=0, padx=10, pady=20)

        self.root.bind_all("<KeyRelease>", self.update_text)
        self.spinbox.bind("<KeyRelease>", self.update_text)
        self.spinbox.bind("<ButtonPress>", self.update_text)

        self.last_updated = None
        self.old_last_updated = None
        self.root.mainloop()

    def display_error(self, message):
        self.error_label.config(text=message)

    def clear_error(self):
        self.error_label.config(text="")

    def update_text(self, event=None):
        input_text = self.input_plaintext.get().strip()
        cipher_text = self.output_ciphertext.get().strip()
        key = self.input_key.get().strip()
        method_name = self.method_var.get()
        method_class = self.methods[method_name]
        spinbox_value = self.spinbox_var.get()

        if event:
            if event.widget == self.input_plaintext:
                last_updated = "plaintext"
            elif event.widget == self.output_ciphertext:
                last_updated = "ciphertext"
            elif event.widget == self.input_key:
                last_updated = "key"
            else:
                last_updated = self.last_updated

            if last_updated != self.last_updated:
                self.old_last_updated = self.last_updated
                self.last_updated = last_updated
        else:
            return

        if not key:
            self.display_error("Key is required.")
            return

        self.clear_error()

        try:
            if self.last_updated == "plaintext" or (self.last_updated == "key" and self.old_last_updated == "plaintext"):
                if not input_text:
                    self.display_error("Plaintext is empty.")
                    return
                encrypted_text = input_text
                for _ in range(spinbox_value):
                    encrypted_text = method_class.encrypt(encrypted_text, key)
                self.output_ciphertext.delete(0, tk.END)
                self.output_ciphertext.insert(0, encrypted_text)

            elif self.last_updated == "ciphertext" or (self.last_updated == "key" and self.old_last_updated == "ciphertext"):
                if not cipher_text:
                    self.display_error("Ciphertext is empty.")
                    return
                decrypted_text = cipher_text
                for _ in range(spinbox_value):
                    decrypted_text = method_class.decrypt(decrypted_text, key)
                self.input_plaintext.delete(0, tk.END)
                self.input_plaintext.insert(0, decrypted_text)

            elif not input_text and not cipher_text:
                self.display_error(
                    "Enter text in either plaintext or ciphertext to proceed.")
            else:
                self.display_error(
                    "Plaintext or Ciphertext must be filled to proceed.")

        except Exception as e:
            self.display_error(f"Error: {str(e)}")

    def clear_entries(self):
        self.input_plaintext.delete(0, tk.END)
        self.input_key.delete(0, tk.END)
        self.output_ciphertext.delete(0, tk.END)
        self.clear_error()
        self.last_updated = None
        self.old_last_updated = None


if __name__ == "__main__":
    Display()
