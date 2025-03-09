import mysql.connector
from config import DB_CONFIG
from encryption import decrypt_password
from tkinter import messagebox
import os
import base64

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def check_users_exist():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0 

def create_user(username, password_hash):
    salt = os.urandom(16)  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, master_password_hash, salt) VALUES (%s, %s, %s)", 
                   (username, password_hash, salt))
    conn.commit()
    conn.close()

def fetch_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, master_password_hash, salt FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def store_password(website, username, encrypted_password):
    print(f"Storing Encrypted Password: {encrypted_password}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (%s, %s, %s)",
                   (website, username, encrypted_password))
    conn.commit()
    conn.close()

def retrieve_password(website, key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, encrypted_password FROM passwords WHERE website = %s", (website,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        print("No password found for this website.")
        return None

    username, encrypted_password = result
    print(f"Retrieved Password: {encrypted_password}")

    try:
        decrypted_password = decrypt_password(encrypted_password, key)
    except Exception:
        print("Warning: Password is already plaintext. Returning as is.")
        decrypted_password = encrypted_password  

    return username, decrypted_password
