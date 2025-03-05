from faker import Faker
from fsi_data_generator.fsi_generators.generate_clabe import generate_clabe


def generate_identification(fake: Faker):
    return [
        fake.aba(),
        fake.iban(),
        fake.swift(),
        fake.bban(),
        generate_clabe()
    ]
