import random

# Function to compute greatest common divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Function to find modular inverse using Extended Euclidean Algorithm
def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to generate a random prime number
def generate_prime(start=100, end=500):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num

# Function to generate RSA key pair
def generate_rsa_keys():
    # For random generation
    # p = generate_prime(100, 500)  
    # q = generate_prime(100, 500)  
    # while p == q:
    #    q = generate_prime(100, 500)  

    p = 383
    q = 443

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Compute the private exponent d
    d = mod_inverse(e, phi)

    return ((e, n), (d, n))  # Public key (e, n), Private key (d, n)

def encrypt_rsa(message, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

def decrypt_rsa(encrypted_message, private_key):
    d, n = private_key
    decrypted = ''.join(chr(pow(char, d, n)) for char in encrypted_message)
    return decrypted

public_key, private_key = generate_rsa_keys()
message = "Cryptography"

ciphertext = encrypt_rsa(message, public_key)
print("Encrypted:", ciphertext)

decrypted_message = decrypt_rsa(ciphertext, private_key)
print("Decrypted:", decrypted_message)
