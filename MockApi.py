# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

from RequestBuilder import SwaggerRequestBuilder, Request


class BaseMockApi:
    def __init__(self):
        self.requests: [Request] = []

    def get_routes(self) -> [tuple]:
        return [{'rule': request.request_url, 'method': request.method} for request in self.requests]

    def process_request(self,
                        user_request,
                        params,
                        status_code,
                        random_seed,
                        default_value,
                        list_size):

        for request in self.requests:
            validated_data = request.validate(url=user_request.url_rule.rule,
                                              method=user_request.method,
                                              req_body=None,
                                              params=params,
                                              status_code=status_code,
                                              random_seed=random_seed,
                                              default_value=default_value,
                                              list_size=list_size)
            if validated_data is not None:
                return validated_data

        raise Exception('Cannot find request to handle the url')

    def show(self):
        for request in self.requests:
            print(f"-> {request.method} {request.request_url}")


class MockApi(BaseMockApi):
    def __init__(self, api_type):
        super().__init__()
        self.api_type = api_type

    def build_requests(self, path):
        if self.api_type == 'swagger':
            self.requests = SwaggerRequestBuilder(path).build()
            return

        raise Exception('Cannot build request for unknown type. Currenly only swagger is supported')
