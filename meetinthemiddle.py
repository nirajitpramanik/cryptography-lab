import random

# Prime modulus and generator (publicly agreed upon values)
p = 23  # A small prime for demonstration (use a large one in real-world scenarios)
g = 5   # A primitive root modulo p

# Alice and Bob's secret keys (normally unknown to each other)
private_a = random.randint(1, p-1)
private_b = random.randint(1, p-1)

# Alice computes her public key and sends it
public_a = pow(g, private_a, p)

# Bob computes his public key and sends it
public_b = pow(g, private_b, p)

# MITM Attack: Mallory intercepts and replaces the keys
# Attacker chooses their own private keys
private_m1 = random.randint(1, p-1)
private_m2 = random.randint(1, p-1)

# Mallory computes public keys for each intercepted transmission
public_m1 = pow(g, private_m1, p)
public_m2 = pow(g, private_m2, p)

# Mallory sends manipulated keys to Alice and Bob
fake_public_a = public_m1  # Instead of sending Bob's key, Mallory sends their own
fake_public_b = public_m2  # Instead of sending Alice's key, Mallory sends their own

# Alice computes the shared secret (with Mallory's key instead of Bob's)
shared_secret_a = pow(fake_public_b, private_a, p)

# Bob computes the shared secret (with Mallory's key instead of Alice's)
shared_secret_b = pow(fake_public_a, private_b, p)

# Mallory computes both shared secrets (as they know both private keys)
shared_secret_m_a = pow(public_a, private_m2, p)
shared_secret_m_b = pow(public_b, private_m1, p)

print("Private keys:")
print(f"Alice's Private Key: {private_a}")
print(f"Bob's Private Key: {private_b}")
print(f"Mallory's Private Keys: {private_m1}, {private_m2}")
print("\nPublic keys:")
print(f"Alice's Public Key: {public_a}")
print(f"Bob's Public Key: {public_b}")
print(f"Mallory's Public Keys: {public_m1}, {public_m2}")

print("\nShared secrets:")
print(f"Shared Secret (Alice - Mallory): {shared_secret_a}")
print(f"Shared Secret (Bob - Mallory): {shared_secret_b}")
print(f"Shared Secret Computed by Mallory with Alice: {shared_secret_m_a}")
print(f"Shared Secret Computed by Mallory with Bob: {shared_secret_m_b}")
