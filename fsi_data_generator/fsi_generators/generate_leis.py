import random
import string


def generate_leis(num_leis=10000):
    leis = []
    for _ in range(num_leis):
        prefix = "549300"
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))
        lei = prefix + random_chars
        leis.append(lei)
    return leis
