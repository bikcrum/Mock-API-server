# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

from Preference import Preference
from RequestBuilder import SwaggerRequestBuilder
from RequestModel import Request


class BaseMockApi:
    def __init__(self, preference):
        self.requests: list[Request] = []
        if preference is None:
            raise Exception('Preference cannot be null')
        self.preference = preference

    def get_routes(self) -> list[tuple]:
        return [{'rule': request.request_url, 'method': request.method} for request in self.requests]

    def process_request(self,
                        user_request,
                        params):

        for request in self.requests:
            validated_data = request.validate(url=user_request.url_rule.rule,
                                              method=user_request.method,
                                              req_body=None,
                                              params=params,
                                              pref=self.preference)
            if validated_data is not None:
                return validated_data

        raise Exception('Cannot find request to handle the url')

    def show(self):
        for request in self.requests:
            print(f"-> {request.method} {request.request_url}")


class MockApi(BaseMockApi):
    def __init__(self, api_type, preference: Preference):
        super().__init__(preference)
        self.api_type = api_type

    def build_requests(self, path):
        if self.api_type == 'swagger':
            self.requests = SwaggerRequestBuilder(path).build()
            return

        raise Exception('Cannot build request for unknown type. Currenly only swagger is supported')
