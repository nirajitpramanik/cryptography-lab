def encrypt_data(input_text, shift):
    encrypted = ""
    
    for i in input_text:
        if i.isalpha():
            new_ascii = ord(i.upper()) + shift
            
            if new_ascii > ord('Z'):
                new_ascii -= 26
            
            encrypted += chr(new_ascii)
        else:
            encrypted += i
            
    return encrypted
    
def decrypt_data(input_text, shift):
    decrypted = ""
    
    for i in input_text:
        if i.isalpha():
            new_ascii = ord(i.upper()) - shift
            
            if new_ascii < ord('A'):
                new_ascii += 26
                
            decrypted += chr(new_ascii)
        else:
            decrypted += i
            
    return decrypted
    
if __name__ == "__main__":
    inp = input("Enter the text to encrypt: ")
    shift = int(input("Enter shift value: "))
    
    encrypted_text = encrypt_data(inp, shift)
    print(f"Encrypted data is: {encrypted_text}")
    
    inp2 = input("Enter text to decrypt: ")
    shift2 = int(input("Enter shift value: "))
    
    decrypted_text = decrypt_data(inp2, shift2)
    print(f"Decrypted data is: {decrypted_text}")
