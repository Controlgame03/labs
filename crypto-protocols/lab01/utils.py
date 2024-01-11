import hashlib

def mod_exp(base, exponent, modulus):
    return (base ** exponent) % modulus

def hash_password(password):
    return int(hashlib.sha256(password.encode()).hexdigest(), 16)

def getReverseNumber(number, p):
    result = 0
    for i in range(1, p):
        if (number * i) % p == 1:
            result = i
        if result != 0:
            break
    return result