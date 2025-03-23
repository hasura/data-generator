from typing import Dict

from data_generator import DataGenerator


def random_record(dg: DataGenerator, fn):
    def get_it(record: Dict, _b, field):
        record.update(fn(record, dg))
        return record.get(field)

    return get_it
