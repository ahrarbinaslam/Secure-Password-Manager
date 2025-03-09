import getpass
import bcrypt
from database import store_password, retrieve_password, fetch_user, create_user, check_users_exist
from encryption import generate_key, encrypt_password, decrypt_password
from authentication import verify_password

def main():
    print("Secure Password Manager")

    if not check_users_exist():
        print("No users found in the database. Let's create an admin account.")
        username = "admin"
        master_password = getpass.getpass("Set a master password: ")

        hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt()).decode()

        create_user(username, hashed_password)
        print(f"Admin user '{username}' created successfully! Now log in.\n")

    username = input("Enter your username: ")
    user = fetch_user(username)

    if not user:
        print("User not found. Exiting...")
        return

    master_password = getpass.getpass("Enter master password: ")

    if verify_password(username, master_password):
        print("Authentication Successful")
        user = fetch_user(username)
        key = generate_key(master_password, user[2]) 
        while True:
            action = input("\nChoose action: (S) Store Password, (R) Retrieve Password, (Q) Quit: ").lower()
            if action == 's':
                website = input("Website: ")
                site_username = input("Username: ")
                site_password = getpass.getpass("Password: ")
                encrypted_password = encrypt_password(site_password, key)
                store_password(website, site_username, encrypted_password)
                print("Password stored securely!")

            elif action == 'r':
                website = input("Website: ")
                result = retrieve_password(website, key)
                if result:
                    print(f"Username: {result[0]}, Password: {result[1]}")
                else:
                    print("No password found for this site.")

            elif action == 'q':
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 'S', 'R', or 'Q'.")

if __name__ == "__main__":
    main()
