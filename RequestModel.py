# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

import json

from Preference import Preference
from Randomizer import Randomizer


class Request:
    def __init__(self):
        self.request_url = None
        self.method = None
        self.parameters = None
        self.request_schema = None
        self.responses: [Response] = None

    def validate(self, url,
                 method,
                 req_body,
                 params,
                 pref: Preference):

        if self.request_url == url and method.lower() == self.method.lower():
            for response in self.responses:
                if response.status_code == str(pref.status_code):
                    return json.dumps(response.get_response_body(pref=pref))

        return None

    def __str__(self):
        return '\n'.join(['Request',
                          f'-> request_url:{self.request_url}',
                          f'-> method:{self.method}',
                          f'-> parameters:{self.parameters}',
                          f'-> request_body:{self.request_schema}',
                          f'-> response:{[str(response) for response in self.responses]}'])


class Response:
    def __init__(self):
        self.status_code = None
        self.response_schema = None

    @staticmethod
    def _get_enum_list(values):
        return f"enum({','.join(map(str, values))})"

    def _data_from_schema(self,
                          prop_name,
                          schema,
                          randomizer: Randomizer,
                          pref: Preference):
        if type(schema) is dict:
            # leaf level
            if schema.get('type') == 'string':
                if prop_name in pref.default_value:
                    return str(pref.default_value[prop_name]), 'string'

                if type(schema.get('enum')) is list:
                    return randomizer.get_random_from_list(schema.get('enum')), \
                           'string.' + self._get_enum_list(schema.get('enum'))

                return randomizer.get_random_string(), 'string'

            if schema.get('type') == 'integer':
                if prop_name in pref.default_value:
                    return int(pref.default_value[prop_name]), 'integer'

                if type(schema.get('enum')) is list:
                    return randomizer.get_random_from_list(schema.get('enum')), \
                           'integer.' + self._get_enum_list(schema.get('enum'))

                return randomizer.get_random_integer(), 'integer'

            if schema.get('type') == 'number':
                if prop_name in pref.default_value:
                    return float(pref.default_value[prop_name]), 'number'

                if type(schema.get('enum')) is list:
                    return randomizer.get_random_from_list(schema.get('enum')), \
                           'number.' + self._get_enum_list(schema.get('enum'))

                return randomizer.get_random_number(), 'number'

            if schema.get('type') == 'boolean':
                if prop_name in pref.default_value:
                    return bool(pref.default_value[prop_name]), 'boolean'

                if type(schema.get('enum')) is list:
                    return randomizer.get_random_from_list(schema.get('enum')), \
                           'boolean.' + self._get_enum_list(schema.get('enum'))

                return randomizer.get_random_boolean(), 'boolean'

            # non-leaf level
            if schema.get('type') == 'object':
                new_dict = {}
                for prop_name in schema['properties']:
                    data = self._data_from_schema(prop_name, schema['properties'][prop_name], randomizer, pref)
                    if type(data) is tuple:
                        new_dict[prop_name] = data[0]
                        if pref.meta:
                            new_dict['@' + prop_name] = data[1]
                    else:
                        new_dict[prop_name] = data

                return new_dict

            if schema.get('type') == 'array':
                size = randomizer.get_random_from_list(pref.list_size)

                items = [self._data_from_schema('items', schema['items'], randomizer, pref) for _ in
                         range(size)]

                return items

        return None

    def get_response_body(self, pref: Preference):

        randomizer = Randomizer()
        if pref.random_seed is not None:
            randomizer.set_random_seed(pref.random_seed)

        return self._data_from_schema(None,
                                      schema=self.response_schema,
                                      randomizer=randomizer,
                                      pref=pref)

    def __str__(self):
        return '\n'.join(['Response',
                          f'-> status_code:{self.status_code}',
                          f'-> response_body:{self.response_schema}'])
