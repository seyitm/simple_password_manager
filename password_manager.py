import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self):
        self.passwords = {}
        self.key = self.generate_key()
        self.fernet = Fernet(self.key)
        self.file_name = "passwords.json"
        self.load_passwords()

    def generate_key(self):
        key_file = "key.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as keyfile:
                key = keyfile.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as keyfile:
                keyfile.write(key)
        return key

    def add_password(self, site, password):
        encrypted_password = self.fernet.encrypt(password.encode()).decode()
        self.passwords[site] = encrypted_password
        self.save_passwords()

    def get_password(self, site):
        encrypted_password = self.passwords.get(site)
        if encrypted_password:
            return self.fernet.decrypt(encrypted_password.encode()).decode()
        return None

    def delete_password(self, site):
        if site in self.passwords:
            del self.passwords[site]
            self.save_passwords()
            return True
        return False

    def save_passwords(self):
        with open(self.file_name, "w") as file:
            json.dump(self.passwords, file)

    def load_passwords(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                self.passwords = json.load(file)

class PasswordManagerGUI:
    def __init__(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.title("Password Manager")

        # Add Password Button
        self.add_button = tk.Button(root, text="Add Password", command=self.add_password)
        self.add_button.pack(pady=10)

        # Get Password Button
        self.get_button = tk.Button(root, text="Get Password", command=self.get_password)
        self.get_button.pack(pady=10)

        # Delete Password Button
        self.delete_button = tk.Button(root, text="Delete Password", command=self.delete_password)
        self.delete_button.pack(pady=10)

    def add_password(self):
        site = simpledialog.askstring("Input", "Enter site name:")
        password = simpledialog.askstring("Input", "Enter password:", show='*')
        if site and password:
            self.manager.add_password(site, password)
            messagebox.showinfo("Success", f"Password for {site} added successfully!")

    def get_password(self):
        site = simpledialog.askstring("Input", "Enter site name:")
        if site:
            password = self.manager.get_password(site)
            if password:
                messagebox.showinfo("Password", f"Password for {site}: {password}")
            else:
                messagebox.showerror("Error", "No password found for this site!")

    def delete_password(self):
        site = simpledialog.askstring("Input", "Enter site name to delete:")
        if site:
            if self.manager.delete_password(site):
                messagebox.showinfo("Success", f"Password for {site} deleted successfully!")
            else:
                messagebox.showerror("Error", "No password found for this site!")

if __name__ == "__main__":
    root = tk.Tk()
    manager = PasswordManager()
    gui = PasswordManagerGUI(root, manager)
    root.mainloop()
