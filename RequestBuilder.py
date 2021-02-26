# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

import json
import random
import string
import os


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
                 status_code,
                 random_seed,
                 default_value,
                 list_size):

        if self.request_url == url and method.lower() == self.method.lower():
            for response in self.responses:
                if response.status_code == str(status_code):
                    return json.dumps(response.get_response_body(
                        random_seed=random_seed,
                        default_value=default_value,
                        list_size=list_size
                    ))

        return None

    def __str__(self):
        return '\n'.join(['Request',
                          f'-> request_url:{self.request_url}',
                          f'-> method:{self.method}',
                          f'-> parameters:{self.parameters}',
                          f'-> request_body:{self.request_schema}',
                          f'-> response:{[str(response) for response in self.responses]}'])


class Randomizer:
    @staticmethod
    def get_random_string():
        return ''.join(random.choices(string.ascii_lowercase, k=10))

    @staticmethod
    def get_random_integer():
        return random.randint(0, 100)

    @staticmethod
    def get_random_number():
        return random.uniform(0, 100)

    @staticmethod
    def get_random_boolean():
        return [True, False][random.randint(0, 1)]


class Response:
    def __init__(self):
        self.status_code = None
        self.response_schema = None

    def _data_from_schema(self,
                          schema,
                          default_value,
                          list_size):
        if type(schema) is dict:
            # leaf level
            if schema.get('type') == 'string':
                return Randomizer().get_random_string()

            if schema.get('type') == 'integer':
                return Randomizer().get_random_integer()

            if schema.get('type') == 'number':
                return Randomizer().get_random_number()

            if schema.get('type') == 'boolean':
                return Randomizer().get_random_boolean()

            # non-leaf level
            if schema.get('type') == 'object':
                new_dict = {}
                for prop in schema['properties']:
                    if prop == 'type':
                        continue
                    if default_value is not None and prop in default_value:
                        new_dict[prop] = default_value[prop]
                    else:
                        new_dict[prop] = self._data_from_schema(schema['properties'][prop], default_value, list_size)
                return new_dict

            if schema.get('type') == 'array':
                size = list_size[random.randint(0, len(list_size) - 1)]

                items = [self._data_from_schema(schema['items'], default_value, list_size) for _ in range(size)]

                return items

        return None

    def get_response_body(self,
                          random_seed,
                          default_value,
                          list_size):
        if random_seed is not None:
            random.seed(random_seed)

        return self._data_from_schema(schema=self.response_schema,
                                      default_value=default_value,
                                      list_size=list_size)

    def __str__(self):
        return '\n'.join(['Response',
                          f'-> status_code:{self.status_code}',
                          f'-> response_body:{self.response_schema}'])


class BaseRequestBuilder:
    def __init__(self, filepath):
        self.filepath = filepath
        self.buffer = open(filepath, 'r')
        os.makedirs('generated', exist_ok=True)
        self.generated = open(os.path.join('generated', os.path.basename(filepath)), 'w')


class SwaggerRequestBuilder(BaseRequestBuilder):
    def __init__(self, filepath):
        super().__init__(filepath)

        data = json.load(self.buffer)
        self.data = self.build_reference(data)
        self.generated.write(json.dumps(self.data, indent=4))

    def build_reference(self, data):
        return self._build_reference(data, data, [])

    def _build_reference(self, _data, data, references):
        if type(data) is dict:
            new_dict = {}
            for key in data:
                if key == '$ref':
                    ref = self._find_schema(_data, data.get(key))

                    # Avoiding cyclic dependency
                    if data.get(key) in references:
                        return f"Cyclic dependency error: Cannot reference {data.get(key)} after {' -> '.join(references)}"

                    new_dict = self._build_reference(_data, ref, references + [data.get(key)])
                    return new_dict
                else:
                    new_dict[key] = self._build_reference(_data, data.get(key), references)
            return new_dict

        if type(data) is list:
            new_list = []
            for val in data:
                new_list.append(self._build_reference(_data, val, references))
            return new_list

        return data

    @staticmethod
    def _find_schema(_data, ref):
        path = ref[2:].split('/')
        ref = _data
        for p in path:
            ref = ref[p]

        return ref

    def build(self) -> [Request]:
        requests = []

        for path, child in self.data['paths'].items():
            for method, _child in child.items():
                request = Request()
                request.method = method

                if 'parameters' in _child:
                    request.parameters = [parameter['name'] for parameter in _child['parameters']]
                    for param in request.parameters:
                        path = path.replace('{' + param + '}', '<' + param + '>')
                request.request_url = path

                if 'responses' in _child:
                    request.responses = []
                    for status_code in _child['responses']:
                        response = Response()
                        response.status_code = status_code

                        if 'content' in _child['responses'][status_code]:
                            for content_type in _child['responses'][status_code]['content']:
                                response.response_schema = _child['responses'][status_code]['content'][content_type][
                                    'schema']
                                break
                        request.responses.append(response)

                if 'requestBody' in _child:
                    if 'content' in _child['requestBody']:
                        for content_type in _child['requestBody']['content']:
                            request.request_schema = _child['requestBody']['content'][content_type]['schema']
                            break

                requests.append(request)

        return requests
