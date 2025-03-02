import random

# SDES Parameters
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

def permute(k, arr, n):
    """Permute input k using the permutation array."""
    return ''.join(k[x - 1] for x in arr)

def left_shift(k, n):
    """Perform a circular left shift on k by n positions."""
    return k[n:] + k[:n]

def xor(a, b):
    """Perform XOR on two binary strings."""
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))

def lookup_in_sbox(s, row, col):
    """Look up value in an S-box."""
    return format(s[row][col], '02b')

def f_k(right, subkey):
    """F-function of SDES."""
    expanded = permute(right, EP, 8)
    xored = xor(expanded, subkey)
    left = xored[:4]
    right = xored[4:]

    # S-box lookup
    row_l = int(left[0] + left[3], 2)
    col_l = int(left[1:3], 2)
    row_r = int(right[0] + right[3], 2)
    col_r = int(right[1:3], 2)
    s0_out = lookup_in_sbox(S0, row_l, col_l)
    s1_out = lookup_in_sbox(S1, row_r, col_r)

    return permute(s0_out + s1_out, P4, 4)

def generate_subkeys(key):
    """Generate subkeys for SDES."""
    k = permute(key, P10, 10)
    left = k[:5]
    right = k[5:]
    # Generate first subkey
    left = left_shift(left, 1)
    right = left_shift(right, 1)
    k1 = permute(left + right, P8, 8)
    # Generate second subkey
    left = left_shift(left, 2)
    right = left_shift(right, 2)
    k2 = permute(left + right, P8, 8)
    return k1, k2

def sdes_encrypt_block(plaintext, key):
    """Encrypt 8 bits using SDES."""
    # Initial permutation
    ip_out = permute(plaintext, IP, 8)
    left = ip_out[:4]
    right = ip_out[4:]

    k1, k2 = generate_subkeys(key)

    new_right = xor(left, f_k(right, k1))
    new_left = right

    final_right = xor(new_left, f_k(new_right, k2))
    final_left = new_right

    return permute(final_right + final_left, IP_INV, 8)

def sdes_decrypt_block(ciphertext, key):
    """Decrypt 8 bits using SDES."""
    ip_out = permute(ciphertext, IP, 8)
    left = ip_out[:4]
    right = ip_out[4:]

    k1, k2 = generate_subkeys(key)

    new_right = xor(left, f_k(right, k2))
    new_left = right

    final_right = xor(new_left, f_k(new_right, k1))
    final_left = new_right

    return permute(final_right + final_left, IP_INV, 8)

class Diffie_Hellman_Algo:
    def __init__(self, prime=None, g=None):
        """Initialize Diffie-Hellman with optional prime and primitive root."""
        if prime is None:
            self.prime = generate_prime()
        else:
            self.prime = prime

        if g is None:
            self.g = find_primroot(self.prime)
        else:
            self.g = g

        # Private key
        self.private_key = random.randint(2, self.prime - 1)
        # Public key
        self.public_key = pow(self.g, self.private_key, self.prime)

    def generate_secret(self, other_public_key):
        """Generate the shared secret using the other party's public key."""
        return pow(other_public_key, self.private_key, self.prime)

    def derive_sdes_key(self, shared_secret):
        """Derive a 10-bit key from the shared secret for SDES."""
        # Use modulo to get a number between 0 and 1023
        key_int = shared_secret % 1024

        # Convert to 10-bit binary string
        return format(key_int, '010b')

    def text_to_binary(self, text):
        """Convert text to binary string."""
        return ''.join(format(ord(c), '08b') for c in text)

    def binary_to_text(self, binary):
        """Convert binary string to text."""
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

    def encrypt_message(self, message, shared_secret):
        """Encrypt a message using SDES with the shared secret."""
        sdes_key = self.derive_sdes_key(shared_secret)

        binary_message = self.text_to_binary(message)

        if len(binary_message) % 8 != 0:
            binary_message += '0' * (8 - (len(binary_message) % 8))

        # Encrypt each 8-bit block
        encrypted_binary = ''
        for i in range(0, len(binary_message), 8):
            block = binary_message[i:i+8]
            encrypted_block = sdes_encrypt_block(block, sdes_key)
            encrypted_binary += encrypted_block

        return encrypted_binary

    def decrypt_message(self, encrypted_binary, shared_secret):
        """Decrypt a message using SDES with the shared secret."""
        sdes_key = self.derive_sdes_key(shared_secret)

        # Decrypt each 8-bit block
        decrypted_binary = ''
        for i in range(0, len(encrypted_binary), 8):
            block = encrypted_binary[i:i+8]
            decrypted_block = sdes_decrypt_block(block, sdes_key)
            decrypted_binary += decrypted_block

        # Convert binary back to text
        return self.binary_to_text(decrypted_binary)

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(min_value=100, max_value=1000):
    """Generate a random prime number within the given range."""
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def find_primroot(prime):
    """Find a primitive root for the given prime number."""
    for g in range(2, prime):
        values = set()
        for i in range(1, prime):
            values.add(pow(g, i, prime))
        if len(values) == prime - 1:
            return g
    return None

def demonstrate_exchange():
    """Demonstrate the Diffie-Hellman key exchange and SDES message exchange."""
    # Use fixed small numbers for demonstration
    prime = 23
    g = 5
    print(f"\nPublic Parameters:")
    print(f"Prime (p): {prime}")
    print(f"Generator (g): {g}")

    # Initialize Alice and Bob
    alice = Diffie_Hellman_Algo(prime, g)
    bob = Diffie_Hellman_Algo(prime, g)

    print(f"\nKey Generation:")
    print(f"Alice's private key: {alice.private_key}")
    print(f"Alice's public key: {alice.public_key}")
    print(f"Bob's private key: {bob.private_key}")
    print(f"Bob's public key: {bob.public_key}")

    # Generate shared secrets
    alice_shared_secret = alice.generate_secret(bob.public_key)
    bob_shared_secret = bob.generate_secret(alice.public_key)
    print(f"\nShared Secrets:")
    print(f"Alice's shared secret: {alice_shared_secret}")
    print(f"Bob's shared secret: {bob_shared_secret}")
    print(f"Secrets match: {alice_shared_secret == bob_shared_secret}")

    # Derive SDES keys
    alice_sdes_key = alice.derive_sdes_key(alice_shared_secret)
    bob_sdes_key = bob.derive_sdes_key(bob_shared_secret)
    print(f"\nDerived SDES Keys (10-bit):")
    print(f"Alice's SDES key: {alice_sdes_key}")
    print(f"Bob's SDES key: {bob_sdes_key}")

    # Message exchange
    message = "Hello Bob"
    print(f"\nMessage Exchange:")
    print(f"Original message: {message}")
    
    # Show binary conversion
    binary_message = alice.text_to_binary(message)
    print(f"Message in binary: {binary_message}")

    # Encryption/Decryption
    encrypted = alice.encrypt_message(message, alice_shared_secret)
    print(f"Encrypted (binary): {encrypted}")
    
    decrypted = bob.decrypt_message(encrypted, bob_shared_secret)
    print(f"Decrypted message: {decrypted}")
    print(f"Message integrity: {message == decrypted}")

if __name__ == "__main__":
    demonstrate_exchange()
 