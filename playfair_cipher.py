def generate_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    used = set()

    for char in key:
        if char not in used and char.isalpha():
            matrix.append(char)
            used.add(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in used:
            matrix.append(char)
            used.add(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None


def prepare_text(text, for_encryption=True):
    text = text.upper().replace('J', 'I')
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = ''
        if i + 1 < len(text):
            b = text[i+1]
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a
            if b:
                result += b
                i += 2
            else:
                i += 1
    if for_encryption and len(result) % 2 == 1:
        result += 'X'
    return result


def encrypt_pair(matrix, a, b):
    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]


def decrypt_pair(matrix, a, b):
    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    if row1 == row2:
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]


def playfair_encrypt(plaintext, key):
    matrix = generate_matrix(key)
    plaintext = prepare_text(plaintext)
    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        ciphertext += encrypt_pair(matrix, a, b)

    return ciphertext


def playfair_decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        plaintext += decrypt_pair(matrix, a, b)

    return plaintext


# Example usage
key = "MONARCHY"
plaintext = "ATTACK"

ciphertext = playfair_encrypt(plaintext, key)
decrypted = playfair_decrypt(ciphertext, key)

print("Original Plaintext:", plaintext)
print("Encrypted:", ciphertext)
print("Decrypted:", decrypted)
