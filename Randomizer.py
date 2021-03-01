# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

import random
import string


class Randomizer:
    def set_random_seed(self, seed_value):
        random.seed(seed_value)

    def get_random_string(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10))

    def get_random_integer(self):
        return random.randint(0, 100)

    def get_random_number(self):
        return random.uniform(0, 100)

    def get_random_boolean(self):
        return [True, False][random.randint(0, 1)]

    def get_random_from_list(self, values):
        return values[random.randint(0, len(values) - 1)]
