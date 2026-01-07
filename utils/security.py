import hashlib
import secrets

def hash_password(password):
    """
    Hash a password using SHA256 with salt.
    Returns: salt$hash
    """
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${pwd_hash}"

def verify_password(password, stored_hash):
    """
    Verify a password against stored hash.
    stored_hash format: salt$hash
    """
    try:
        salt, pwd_hash = stored_hash.split('$')
        new_hash = hashlib.sha256((salt + password).encode()).hexdigest()
        return new_hash == pwd_hash
    except:
        return False