from enum import IntEnum
from functools import wraps
from typing import List, Tuple

from flask import json
from flask import request


class Response(IntEnum):
    # API basics
    BAD_REQUEST = 0
    INVALID_OBJECT_ID = 1

    # Authorization related
    UNAUTHORIZED = 100
    BAD_CREDENTIALS = 101
    USER_EXISTS = 102

    # Queue
    TRACK_UNAVAILABLE = 200
    NOT_IN_QUEUE = 201

    # Upload
    TRACK_EXISTS = 300
    PLUGIN_ERROR = 301
    INVALID_PLUGIN = 302

# TODO: user readable description for error enum


def expect(arguments: List[Tuple[str, type]]):

    def wrapper(function):

        @wraps(function)
        def wrapped(*args, **kwargs):

            for arg_name, arg_type in arguments:
                argument = request.args.get(arg_name)

                if argument is None:
                    return json.dumps({
                        'success': False,
                        'reason': Response.BAD_REQUEST
                    })

                if arg_type is not None:
                    try:
                        argument = arg_type(argument)
                    except:
                        return json.dumps({
                            'success': False,
                            'reason': Response.BAD_REQUEST
                        })

                kwargs[arg_name] = argument

            return function(*args, **kwargs)

        return wrapped

    return wrapper


def expect_optional(arguments: List[Tuple[str, type]]):

    def wrapper(function):

        @wraps(function)
        def wrapped(*args, **kwargs):

            for arg_name, arg_type in arguments:
                argument = request.args.get(arg_name)

                if argument is None: continue

                if arg_type is not None:
                    try:
                        argument = arg_type(argument)
                    except:
                        return json.dumps({
                            'success': False,
                            'reason': Response.BAD_REQUEST
                        })

                kwargs[arg_name] = argument

            return function(*args, **kwargs)

        return wrapped

    return wrapper
