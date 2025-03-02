from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def generate_key(key_size):
    """Generates a key with the requested key size (128, 192, or 256 bits)."""
    if key_size not in [128, 192, 256]:
        raise ValueError("Key size must be 128, 192, or 256 bits.")
    
    key = os.urandom(key_size // 8)  # Convert bits to bytes
    return key  # Return key without padding since it's already the correct length

def encrypt_aes(plaintext, key):
    """Encrypts a plaintext string using AES CBC mode."""
    iv = os.urandom(16)  # AES requires a 16-byte IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return iv + ciphertext  # Return IV + ciphertext for decryption

def decrypt_aes(ciphertext, key):
    """Decrypts an AES CBC-mode encrypted ciphertext."""
    iv = ciphertext[:16]  # Extract IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return plaintext.decode()

# Key Expansion (if required) - AES handles this internally with the provided key size.
def key_expansion(key):
    """Simulate AES key expansion."""
    cipher = AES.new(key, AES.MODE_ECB)  # Using ECB mode for demonstration
    expanded_key = cipher._key
    return expanded_key

# Example Usage
if __name__ == "__main__":
    # User input for key size and plaintext
    key_size = int(input("Enter key size (128, 192, or 256 bits): "))
    if key_size not in [128, 192, 256]:
        print("Invalid key size! Please enter 128, 192, or 256 bits.")
        exit()

    # Enter the key as plaintext, convert it to hex and check length
    key_plaintext = input(f"Enter a key (plaintext) to convert to hex for {key_size}-bit key: ")
    # Convert the key (plaintext) to hex
    key_hex = key_plaintext.encode().hex()

    # Check if the hex key length is valid for the selected key size
    if len(key_hex) != key_size // 4:
        print(f"Invalid key length! The key must be {key_size // 4} hexadecimal characters.")
        exit()

    key = bytes.fromhex(key_hex)  # Convert the hex key to bytes

    # Enter plaintext
    plaintext = input("Enter the plaintext to encrypt: ")

    # Encrypt and Decrypt using AES
    ciphertext = encrypt_aes(plaintext, key)
    decrypted_message = decrypt_aes(ciphertext, key)

    # Output results
    print(f"Encrypted (Hex): {ciphertext.hex()}")
    print(f"Decrypted: {decrypted_message}")
