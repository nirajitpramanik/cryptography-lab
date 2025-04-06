import random
import hashlib

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def mod_inv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def is_prime(n, k=40):  # Increased iterations for better primality test
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Find r and d such that n-1 = d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = mod_exp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        # Ensure we get a number with exactly 'bits' bits
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Set MSB and LSB to 1
        if is_prime(num):
            return num

def generate_keys():
    # Generate a 160-bit prime q
    q = generate_prime(160)
    
    # Generate p such that p = k*q + 1 for some k
    # This ensures q divides p-1
    k = random.getrandbits(352)  # 512-160=352 bits for k
    p = q * k + 1
    
    # Find a value of k that makes p prime
    while not is_prime(p) or p.bit_length() < 512:
        k = random.getrandbits(352)
        p = q * k + 1
    
    # Find a generator h such that g = h^((p-1)/q) mod p ≠ 1
    h = random.randint(2, p-1)
    g = mod_exp(h, (p-1)//q, p)
    while g == 1:
        h = random.randint(2, p-1)
        g = mod_exp(h, (p-1)//q, p)
    
    # Generate private and public keys
    x = random.randint(1, q-1)  # Private key
    y = mod_exp(g, x, p)        # Public key
    
    return (p, q, g, y), x

# Signing function
def sign(message, p, q, g, x):
    hash_value = int(hashlib.sha256(message.encode()).hexdigest(), 16) % q
    
    while True:
        k = random.randint(1, q-1)
        r = mod_exp(g, k, p) % q
        if r == 0:
            continue
        
        k_inv = mod_inv(k, q)
        s = (k_inv * (hash_value + x * r)) % q
        if s != 0:
            break
    
    return r, s

# Verification function
def verify(message, signature, p, q, g, y):
    r, s = signature
    if not (0 < r < q and 0 < s < q):
        return False
    
    hash_value = int(hashlib.sha256(message.encode()).hexdigest(), 16) % q
    w = mod_inv(s, q)
    u1 = (hash_value * w) % q
    u2 = (r * w) % q
    v = ((mod_exp(g, u1, p) * mod_exp(y, u2, p)) % p) % q
    
    return v == r

if __name__ == "__main__":
    print("Generating DSA keys (this may take a moment)...")
    public_key, private_key = generate_keys()
    p, q, g, y = public_key
    print(f"Public Key: p={p} (bits: {p.bit_length()})")
    print(f"            q={q} (bits: {q.bit_length()})")
    print(f"            g={g}")
    print(f"            y={y}")
    print(f"Private Key: x={private_key}")

    message = "Hello, this is a test message."
    signature = sign(message, public_key[0], public_key[1], public_key[2], private_key)
    print("Signature (r, s):", signature)

    is_valid = verify(message, signature, *public_key)
    print("Verification result:", is_valid)