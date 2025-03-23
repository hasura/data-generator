from typing import Union

from faker import Faker

fake = Faker()


def unique_list(d: Union[list, tuple]):
    # Ensure `d` is a tuple (convert if it's a list)
    if isinstance(d, list):
        d = tuple(d)
    elif not isinstance(d, tuple):
        raise TypeError("The input must be a list or a tuple.")

    def list_values(_a, _b, _c):
        v = fake.unique.random_element(d)
        return v

    return list_values
