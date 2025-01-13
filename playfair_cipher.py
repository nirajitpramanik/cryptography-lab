import time
import json

def generate_key_table(key):
    """
    Generates the key cipher value.
    """
    key = ''.join(sorted(set(key), key=lambda x: key.index(x))).upper()
    
    key_table = []
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    
    for char in alphabet:
        if char not in key:
            key += char

    for i in range(5):
        key_table.append(key[i*5:(i+1)*5])
    
    return key_table

def prepare_message(message):
    """
    Prepares the message.
    """
    message = message.upper().replace("J", "I").replace(" ", "")
    if len(message) % 2 != 0:
        message += 'X'
    return message

def find_position(char, key_table):
    """
    Find the position of the alphabet in the cipher.
    """
    for i in range(5):
        for j in range(5):
            if key_table[i][j] == char:
                return i, j

def encrypt_message(message, key_table):
    """
    Encrypt the message using the cipher created.
    """
    encrypted_message = ""
    
    for i in range(0, len(message), 2):
        first_char = message[i]
        second_char = message[i+1]
        
        r1, c1 = find_position(first_char, key_table)
        r2, c2 = find_position(second_char, key_table)
        
        if r1 == r2:
            encrypted_message += key_table[r1][(c1 + 1) % 5]
            encrypted_message += key_table[r2][(c2 + 1) % 5]
        elif c1 == c2:
            encrypted_message += key_table[(r1 + 1) % 5][c1]
            encrypted_message += key_table[(r2 + 1) % 5][c2]
        else:
            encrypted_message += key_table[r1][c2]
            encrypted_message += key_table[r2][c1]
    
    return encrypted_message

def decrypt_message(message, key_table):
    """
    Decrypt the message using the cipher created.
    """
    decrypted_message = ""
    for i in range(0, len(message), 2):
        first_char = message[i]
        second_char = message[i+1]
        
        r1, c1 = find_position(first_char, key_table)
        r2, c2 = find_position(second_char, key_table)
        
        if r1 == r2:
            decrypted_message += key_table[r1][(c1 - 1) % 5]
            decrypted_message += key_table[r2][(c2 - 1) % 5]
        elif c1 == c2:
            decrypted_message += key_table[(r1 - 1) % 5][c1]
            decrypted_message += key_table[(r2 - 1) % 5][c2]
        else:
            decrypted_message += key_table[r1][c2]
            decrypted_message += key_table[r2][c1]
    
    return decrypted_message

if __name__ == "__main__":
    key = input("Enter the key: ")
    message = input("Enter the message to encrypt: ")
    
    key_table = generate_key_table(key)
    
    print(json.dumps(key_table, indent = 2))
    
    prepared_message = prepare_message(message)
    
    start_time = time.time()
    encrypted_message = encrypt_message(prepared_message, key_table)
    end_time = time.time()
    print(f"Encrypted message: {encrypted_message}")
    print(f"Encryption time: {end_time - start_time:.6f} seconds")
    
    message_to_decrypt = input("Enter the message to decrypt: ")
    start_time = time.time()
    decrypted_message = decrypt_message(message_to_decrypt, key_table)
    end_time = time.time()
    print(f"Decrypted message: {decrypted_message}")
    print(f"Decryption time: {end_time - start_time:.6f} seconds")
