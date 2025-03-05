from faker import Faker
fake = Faker()
def text_list(d):
    def list_values(a,b,c):
        v = fake.random_element(d)
        return v
    return list_values
