import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from config import DB_CONFIG  
from encryption import encrypt_password, decrypt_password, generate_key
from database import store_password, retrieve_password, fetch_user
import mysql.connector


MASTER_PASSWORD = simpledialog.askstring("Master Password", "Enter your master password:", show="*")

if not MASTER_PASSWORD:
    messagebox.showerror("Error", "Master password is required!")
    exit()

user = fetch_user("admin") 
if not user:
    messagebox.showerror("Error", "User not found!")
    exit()

user_salt = user[2] 
encryption_key = generate_key(MASTER_PASSWORD, user_salt)  

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    if not website or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    encrypted_password = encrypt_password(password, encryption_key)
    store_password(website, username, encrypted_password)
    messagebox.showinfo("Success", "Password saved securely!")

def retrieve_password_gui():
    website = website_entry.get()
    if not website:
        messagebox.showerror("Error", "Please enter a website.")
        return
    
    result = retrieve_password(website, encryption_key) 
    if result:
        username, decrypted_password = result
        messagebox.showinfo("Retrieved Password", f"Username: {username}\nPassword: {decrypted_password}")
    else:
        messagebox.showerror("Error", "No password found for this website.")


root = tk.Tk()
root.title("Secure Password Manager")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

title_label = tk.Label(root, text="🔐 Secure Password Manager", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=5)

tk.Label(frame, text="Website:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Label(frame, text="Username:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Label(frame, text="Password:", font=("Arial", 10), bg="#f5f5f5").grid(row=2, column=0, sticky="w", padx=10, pady=5)

website_entry = tk.Entry(frame, width=30)
username_entry = tk.Entry(frame, width=30)
password_entry = tk.Entry(frame, width=30, show="*")

website_entry.grid(row=0, column=1, padx=10, pady=5)
username_entry.grid(row=1, column=1, padx=10, pady=5)
password_entry.grid(row=2, column=1, padx=10, pady=5)

button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack(pady=10)

save_button = tk.Button(button_frame, text="Save Password", command=save_password, bg="#4CAF50", fg="white", font=("Arial", 10), width=18, height=1)
retrieve_button = tk.Button(button_frame, text="Retrieve Password", command=retrieve_password_gui, bg="#2196F3", fg="white", font=("Arial", 10), width=18, height=1)

save_button.grid(row=0, column=0, padx=10, pady=5)
retrieve_button.grid(row=0, column=1, padx=10, pady=5)

root.mainloop()
