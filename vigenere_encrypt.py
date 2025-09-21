import random, string

def generate_key(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def vignere_encrypt(text, key):
    encrypted = []
    for i, c in enumerate(text):
        shift = ord(key[i % len(key)].upper()) - 65
        if c.isalpha():
            base = 65 if c.isupper() else 97
            encrypted.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            encrypted.append(c)
    return ''.join(encrypted)

password = input("Enter password: ")
key = generate_key(len(password))
ciphertext = vignere_encrypt(password, key)
print("Random key:", key)
print("Encrypted password:", ciphertext)
