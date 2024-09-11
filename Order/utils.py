import secrets
import string

def generate_order_code(length=12):
    """Generate a unique order code with specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_str_digit(length=12):
    """Generate a random integer with specified length."""
    return ''.join(secrets.choice(string.digits) for _ in range(length))