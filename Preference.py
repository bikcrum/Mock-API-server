# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

class Preference:
    def __init__(self,
                 status_code,
                 random_seed,
                 default_value,
                 list_size,
                 meta):
        self.status_code = status_code
        self.random_seed = random_seed
        self.default_value = default_value
        self.list_size = list_size
        self.meta = meta
