from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def encrypt(key, plaintext):
    """
    Encrypt plaintext using DES algorithm.
    """
    cipher = DES.new(key, DES.MODE_ECB)  
    padded_text = pad(plaintext.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext


def decrypt(key, ciphertext):
    """
    Decrypt ciphertext using DES algorithm.
    """
    cipher = DES.new(key, DES.MODE_ECB) 
    decrypted_text = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return decrypted_text.decode()


if __name__ == "__main__":
    key = b"abcdefgh"
    plaintext = "Hello, DES encryption!"

    print("Original Text:", plaintext)

    encrypted = encrypt(key, plaintext)
    print("Encrypted Text:", encrypted)

    decrypted = decrypt(key, encrypted)
    print("Decrypted Text:", decrypted)
