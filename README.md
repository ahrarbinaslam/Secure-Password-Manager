# Secure-Password-Manager

Secure Password Manager is a Python-based application that allows users to store, encrypt, and retrieve passwords securely. It supports AES-GCM encryption, bcrypt authentication, and two-factor authentication (2FA) with OTP. Users can interact with the application via both a command-line interface (CLI) and a graphical user interface (GUI) using Tkinter.

# Features

1. User Authentication

Supports multiple users with individual encryption keys.

2. Password Management

Store and encrypt passwords using AES-GCM.
Retrieve and decrypt stored passwords.

3. Graphical and CLI Support

Intuitive GUI built with Tkinter.
Command-line interface for users preferring terminal interaction.

4. Database Integration

Uses MariaDB for storing user credentials and encrypted passwords.
Secure storage with password salting.


# Installation

1. Clone the Repository

git clone https://github.com/ahrarbinaslam/Secure-Password-Manager.git
cd Secure-Password-Manager

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows

3. Install Dependencies

pip install -r requirements.txt

4. Set Up the Database
Ensure MariaDB/MySQL is installed and running. Then, create a database:

CREATE DATABASE password_manager;
USE password_manager;

Run the following commands to create the necessary tables:

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    master_password_hash TEXT NOT NULL,
    salt BLOB NOT NULL,
);

CREATE TABLE passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    encrypted_password TEXT NOT NULL
);

# Usage

1. Running the CLI Version

To start the CLI version of the password manager:

python main.py

2. Running the GUI Version

To start the GUI version:

python gui.py

