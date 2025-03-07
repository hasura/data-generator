from faker import Faker
fake = Faker()


def unique_text_list(d):
    def list_values(a,b,c):
        v = fake.unique.random_element(d)
        return v
    return list_values
