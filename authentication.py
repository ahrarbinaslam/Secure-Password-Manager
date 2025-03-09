import bcrypt
from database import fetch_user

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(username, input_password):
    user = fetch_user(username)
    if user:
        stored_hash = user[1]
        return bcrypt.checkpw(input_password.encode(), stored_hash.encode())
    return False