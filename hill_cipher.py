import numpy as np
import math

def text_to_numbers(text):
    text = text.upper().replace(" ", "")  
    return [ord(char) - ord('A') for char in text]

def numbers_to_text(numbers):
    return ''.join(chr(num + ord('A')) for num in numbers)

def generate_key_matrix(key, size):
    key = key.upper().replace(" ", "")
    key_numbers = [ord(char) - ord('A') for char in key]
    
    if len(key_numbers) != size * size:
        raise ValueError(f"Key must have exactly {size * size} characters for a {size}x{size} matrix.")
    
    key_matrix = np.array(key_numbers).reshape(size, size)
    return key_matrix

def matrix_inverse(matrix, mod=26):
    det = int(np.linalg.det(matrix))  
    det_inv = pow(det, -1, mod)  
    
    matrix_adj = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix)) % mod
    matrix_inv = (det_inv * matrix_adj) % mod
    return matrix_inv.astype(int)

def encrypt_data(plaintext, key_matrix):
    
    plaintext_numbers = text_to_numbers(plaintext)
    size = key_matrix.shape[0]
    
    while len(plaintext_numbers) % size != 0:
        plaintext_numbers.append(0) 

    ciphertext_numbers = []
    for i in range(0, len(plaintext_numbers), size):
        block = plaintext_numbers[i:i+size]
        encrypted_block = np.dot(key_matrix, block) % 26
        ciphertext_numbers.extend(encrypted_block)

    ciphertext = numbers_to_text(ciphertext_numbers)
    return ciphertext

def decrypt_data(ciphertext, key_matrix):
    key_matrix_inv = matrix_inverse(key_matrix, mod=26)
    
    ciphertext_numbers = text_to_numbers(ciphertext)
    size = key_matrix.shape[0]
    
    decrypted_numbers = []
    for i in range(0, len(ciphertext_numbers), size):
        block = ciphertext_numbers[i:i+size]
        decrypted_block = np.dot(key_matrix_inv, block) % 26
        decrypted_numbers.extend(decrypted_block)

    decrypted_text = numbers_to_text(decrypted_numbers)
    return decrypted_text

if __name__ == "__main__":
    key = input("Enter the key: ")
    
    size = int(math.sqrt(len(key)))
    
    if size * size != len(key):
        raise ValueError("Key length must be a perfect square.")
    
    print(f"Key length: {len(key)}, Matrix size: {size}x{size}")

    plaintext = input(f"Enter the plaintext (length should be {size}): ")
    
    if len(plaintext) != size:
        raise ValueError(f"Plaintext length must be exactly {size} characters.")

    key_matrix = generate_key_matrix(key, size)
    
    encrypted_message = encrypt_data(plaintext, key_matrix)
    print(f"Encrypted message: {encrypted_message}")
    
    encrypted = input("Enter encrypted data to decrypt: ")

    decrypted_message = decrypt_data(encrypted, key_matrix)
    print(f"Decrypted message: {decrypted_message}")
