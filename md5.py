import struct
import binascii
import math

def md5(message: bytes) -> bytes:
    """MD5 hash function implementation."""
    
    def left_rotate(x, amount):
        # 1. Perform left rotation on 32-bit integer
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF
    
    # 2. Define shift amounts and constants (computed using sine function)
    s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    K = [int((1 << 32) * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
    
    # 3. Append padding and length to the message
    message_length = len(message) * 8
    message += b'\x80'  # Append a single 1-bit followed by zeros
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', message_length)  # Append original length (64-bit little-endian)
    
    # 4. Initialize MD5 buffer variables
    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    
    # 5. Process each 512-bit chunk
    for chunk_offset in range(0, len(message), 64):
        M = struct.unpack('<16I', message[chunk_offset:chunk_offset+64])
        A, B, C, D = a0, b0, c0, d0
        
        # 6. Perform main MD5 transformation loop
        for i in range(64):
            if i < 16:
                F = (B & C) | (~B & D)
                g = i
            elif i < 32:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif i < 48:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                F = C ^ (B | ~D)
                g = (7 * i) % 16
            
            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, s[i])) & 0xFFFFFFFF
        
        # 7. Update hash state with new values
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF
    
    # 8. Return final MD5 hash as packed bytes
    return struct.pack('<4I', a0, b0, c0, d0)

def generate_md5(message: str) -> str:
    """Generate an MD5 hash for a given message."""
    message_bytes = message.encode('utf-8')
    hash_bytes = md5(message_bytes)
    return binascii.hexlify(hash_bytes).decode('utf-8')

# Example usage
if __name__ == "__main__":
    message = "Cryptography is fun."
    hash_value = generate_md5(message)
    print(f"Message: {message}")
    print(f"MD5 Hash: {hash_value}")