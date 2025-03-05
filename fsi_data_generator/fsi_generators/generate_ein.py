from faker import Faker

fake = Faker()

def generate_ein():
  """Generates a valid EIN."""
  # EIN format is 00-0000000
  return f"{fake.random_int(0, 99):02d}-{fake.random_int(0, 9999999):07d}"

def generate_eins(num_eins=10000):
    eins = set()
    for _ in range(num_eins):
        eins.add(generate_ein())
    return list(eins)

fake_eins = generate_eins()
