from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import binascii

def bytes_to_bin(b):
    return ''.join(f'{byte:08b}' for byte in b)

def des_round_output(plaintext, key, round_k):
    from Crypto.Cipher import DES
    from Crypto.Cipher._mode_ecb import _create_ecb_cipher

    assert 1 <= round_k <= 16, "Round must be between 1 and 16"

    # Pad plaintext to 8 bytes
    plaintext = pad(plaintext.encode(), 8)
    des_cipher = _create_ecb_cipher(DES, key, None)

    # Manually do the initial permutation
    block = des_cipher.encrypt(plaintext)  # Just to set things up
    L, R = des_cipher._l, des_cipher._r

    print(f"Initial L0: {L:032b}")
    print(f"Initial R0: {R:032b}")

    for i in range(1, round_k + 1):
        L, R = R, L ^ des_cipher._round_encrypt(i, R)
        print(f"Round {i} Output - L{i}: {L:032b}, R{i}: {R:032b}")

    return L, R

# Example usage:
plaintext = "ABCDEFGH"
key = b"12345678"  # 8-byte DES key

k = 3  # Example: output after 3rd round
des_round_output(plaintext, key, k)

# 12. DES Shifts

# Number of left shifts for each of the 16 rounds in DES
left_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Example: initial 56-bit key split into two 28-bit halves
def left_rotate(bits, n):
    return bits[n:] + bits[:n]

def simulate_key_shifts(C0, D0):
    round_keys = []
    for i in range(16):
        shift = left_shifts[i]
        C0 = left_rotate(C0, shift)
        D0 = left_rotate(D0, shift)
        round_keys.append((C0, D0))
        print(f"Round {i+1}: C = {C0}, D = {D0}")
    return round_keys

# Dummy 28-bit strings for testing (normally you'd get these from PC-1 permutation)
C0 = "1111000011001100101010101111"
D0 = "0101010100001111000011001100"

simulate_key_shifts(C0, D0)