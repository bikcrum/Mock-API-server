# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

import json
import os

from RequestModel import Response, Request


class BaseRequestBuilder:
    def __init__(self, filepath):
        self.filepath = filepath
        self.buffer = open(file=filepath, mode='r', encoding='utf-8')
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

    def build(self) -> list[Request]:
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
