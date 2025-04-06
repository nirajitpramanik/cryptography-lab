def rail_fence_encrypt(text, rails):
    rail = [[] for _ in range(rails)]
    counter = 0
    direction = 1  # 1 = down, -1 = up

    for char in text:
        rail[counter].append(char)

        if counter == 0:
            direction = 1
        elif counter == rails - 1:
            direction = -1

        counter += direction

    # Combine rails
    return ''.join([''.join(r) for r in rail])


def rail_fence_decrypt(ciphertext, rails):
    n = len(ciphertext)
    rail = [['\n' for _ in range(n)] for _ in range(rails)]
    # Mark the zigzag path
    row, direction = 0, 1
    for i in range(n):
        rail[row][i] = '*'
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction

    # Fill the ciphertext into the zigzag path
    index = 0
    for r in range(rails):
        for c in range(n):
            if rail[r][c] == '*' and index < n:
                rail[r][c] = ciphertext[index]
                index += 1
    print(rail)

    # Read the zigzag path to decrypt
    result = ''
    row, direction = 0, 1
    for i in range(n):
        result += rail[row][i]
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction

    return result

plaintext = "HELLOWORLD"
rails = 3

encrypted = rail_fence_encrypt(plaintext, rails)
print("Encrypted:", encrypted)

decrypted = rail_fence_decrypt(encrypted, rails)
print("Decrypted:", decrypted)
