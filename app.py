# license: SEE LICENSE IN LICENSE.md [MUST NOT BE REMOVED]

import argparse

from flask import Flask, Response
from flask import request

from MockApi import MockApi


def build_arguments():
    parser = argparse.ArgumentParser(description='Options for mock responses')
    parser.add_argument('-s',
                        '--source',
                        required=True,
                        help='(Required) API reference source file path.')
    parser.add_argument('-p',
                        '--port',
                        type=str,
                        help='(Optional,default=5000) Port number the app runs on.',
                        default=5000)
    parser.add_argument('-t',
                        '--type',
                        type=str,
                        help='(Optional,default=\'swagger\') Type of API reference. Currently only supports Swagger.', choices=['swagger'],
                        default='swagger')
    parser.add_argument('-sc',
                        '--status_code',
                        type=int,
                        help='(Optional,default=200) Generates responses with status code provided',
                        default=200)
    parser.add_argument('-r',
                        '--random_seed',
                        type=int,
                        help='(Optional) Generates random responses based on seed value')
    parser.add_argument('-d',
                        '--default_value',
                        nargs='+',
                        help='(Optional) Sets default values in response body. Format key=value')
    parser.add_argument('-l',
                        '--list_size',
                        nargs='+',
                        type=int,
                        help='(Optional,default=[2]) Sets default size of list in response body',
                        default=[2])

    return parser.parse_args()


def process_request(**kwargs):
    return Response(mp.process_request(user_request=request,
                                       params=kwargs,
                                       status_code=args.status_code,
                                       random_seed=args.random_seed,
                                       default_value=dict([value.split('=') for value in args.default_value])
                                       if args.default_value is not None else None,
                                       list_size=args.list_size),
                    mimetype='application/json',
                    status=args.status_code if args.status_code is not None else 200)


if __name__ == '__main__':
    args = build_arguments()
    print(args)

    mp = MockApi(api_type=args.type)
    mp.build_requests(args.source)

    app = Flask(__name__)

    for route in mp.get_routes():
        view_func = app.route(route['rule'], methods=[route['method']])(process_request)

    print('Active endpoints')
    mp.show()

    app.run(port=args.port)