from faker import Faker
fake = Faker()
def text_list(d, lower=False):
    def list_values(_a,_b,_c):
        v = fake.random_element(d)
        if lower:
            v = v.lower()
        return v
    return list_values
