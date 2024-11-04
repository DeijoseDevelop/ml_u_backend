import json
import typing
import enum

import http
import flask


class Status(enum.Enum):
    OK_200 = 200
    CREATED_201 = 201
    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    NOT_FOUND_404 = 404
    INTERNAL_SERVER_ERROR_500 = 500


class Response(flask.Response):
    def __init__(
        self,
        response: typing.Iterable[bytes] | bytes | typing.Iterable[str] | str | None = None,
        status: int | str | http.HTTPStatus | Status | None = Status.OK_200,
        headers: typing.Mapping[str, str | typing.Iterable[str]] | typing.Iterable[tuple[str, str]] | None = None,
        mimetype: str | None = "application/json",
    ):
        if isinstance(response, (dict, list)):
            response = json.dumps(response)

        if isinstance(status, Status):
            status = status.value

        super().__init__(response, status, headers, mimetype)
