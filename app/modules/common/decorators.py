import os

import flask
from dotenv import load_dotenv

from .utils import Response, Status

load_dotenv()


def x_api_key_required(method):
    def wrapper(*args, **kwargs):
        x_api_key = flask.request.headers.get("X-Api-Key", False)

        if not x_api_key:
            return Response({"message": 'X-API-KEY header is required'}, status=Status.UNAUTHORIZED_401)

        if x_api_key != os.getenv("X_API_KEY"):
            return Response({"message": 'X-API-KEY invalid'}, status=Status.UNAUTHORIZED_401)

        return method(*args, **kwargs)

    return wrapper