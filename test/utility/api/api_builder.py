from typing import Union

import httpx
from pydantic.dataclasses import dataclass

api_endpoint = {
    "login":"/api/v1/login"
}

class RestApiBuilder(object):
    header = ({
        "Content-Type": "application/json",
        "Accept": "*/*"
    })

    def __init__(self,
                 host: str,
                 port: str,
                 context: dict):
        self.default_header = dict(self.header)

        # Initalize the base url
        self.base_url = f"host:port"

        # Initialize the request
        request = context["request"] if "request" in context.keys() else Exception("Cant find request dict")
        req_keys = request.keys()
        #TO DO: need to refactor, using pydantic for proper constructor handling
        self.method = context["method"] if "method" in req_keys else "GET"
        self.endpoint = context["endpoint"] if "endpoint" in req_keys else ""
        self.header = context["header"] if "header" in req_keys else self.default_header
        self.payload = context["payload"] if "payload" in req_keys else None
        self.queryparam = context["queryparam"] if "queryparam" in req_keys else ""
        self.path = context["path"] if "path" in req_keys else ""

    def get_data(self) -> dict:
        return {
            "method": self.method,
            "endpoint": self.endpoint,
            "header": self.header,
            "payload": self.payload,
            "queryparam": self.queryparam,
            "path": self.path
        }

    #send the request using all information
    def send(self) -> str:
        pass