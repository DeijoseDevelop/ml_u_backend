import abc

import flasgger


class APIView(abc.ABC, flasgger.SwaggerView):
    pass


class BaseController(abc.ABC):
    pass


class Service(abc.ABC):
    pass


class Detector(abc.ABC):
    pass


class Manager(abc.ABC):
    pass