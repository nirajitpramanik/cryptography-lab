def encrypt(plaintext, key):
    """
    Encrypts the plaintext using a columnar transposition cipher.
    """
    ciphertext = [""] * key

    # Loop through each column in the key
    for column in range(key):
        pointer = column

        # Append characters in the column to the ciphertext
        while pointer < len(plaintext):
            ciphertext[column] += plaintext[pointer]
            pointer += key

    return "".join(ciphertext)


def decrypt(ciphertext, key):
    """
    Decrypts the ciphertext using a columnar transposition cipher.
    """
    # Calculate the number of rows and shaded boxes
    num_rows = -(-len(ciphertext) // key) 
    num_shaded_boxes = (num_rows * key) - len(ciphertext)

    plaintext = [""] * num_rows
    col = 0
    row = 0

    for symbol in ciphertext:
        plaintext[row] += symbol
        row += 1

        if (row == num_rows) or (row == num_rows - 1 and col >= key - num_shaded_boxes):
            row = 0
            col += 1

    return "".join(plaintext)


if __name__ == "__main__":
    plaintext = input("Enter the plaintext: ")
    key = 8

    encrypted_text = encrypt(plaintext, key)
    print(f"Encrypted Text: {encrypted_text}")

    decrypted_text = decrypt(encrypted_text, key)
    print(f"Decrypted Text: {decrypted_text}")
