import string
import random

def generate_link(num, length=8):
    alphabet = string.digits + string.ascii_letters

    base = len(alphabet)
    encoded = []
    while num:
        num, rem = divmod(num, base)
        encoded.append(alphabet[rem])
    while len(encoded) < length:
        
        encoded.append(random.choice(alphabet))
    return ''.join(reversed(encoded))





    