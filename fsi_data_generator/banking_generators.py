from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.consumer_banking import consumer_banking
from fsi_data_generator.fsi_generators.consumer_lending import consumer_lending
from fsi_data_generator.fsi_generators.credit_cards import credit_cards
from fsi_data_generator.fsi_generators.enterprise import enterprise
from fsi_data_generator.fsi_generators.mortgage_services import mortgage_services
from fsi_data_generator.fsi_generators.small_business_banking import small_business_banking
from fsi_data_generator.fsi_generators.wildcards import wildcards

dg = None
def custom_generators(gen: DataGenerator):
    global dg
    dg = gen
    return (
        wildcards +
        enterprise(dg) +
        small_business_banking(dg) +
        consumer_lending(dg) +
        mortgage_services(dg) +
        credit_cards(dg) +
        consumer_banking(dg)
    )
