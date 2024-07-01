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
        context_keys = context.keys()
        request = context["request"] if "request" in context.keys() else Exception("Cant find request dict")
        req_keys = request.keys()

        # Initalize the base url
        base_url = f"host:port"
        endpoint = context["endpoint"] if "endpoint" in context_keys else ""

        # Initialize the method and endpoint
        #TO DO: need to refactor, using pydantic for proper constructor handling
        self.method = context["method"] if "method" in context_keys else "GET"

        # Initialize the request
        self.path = request["path"] if "path" in req_keys else None
        self.url = base_url + endpoint
        if ("header" in req_keys):
            if request["header"] is not None :
                self.header = request["header"]
            else:
                self.header = self.default_header

        self.payload = request["payload"] if ("payload" in req_keys) and (self.method != "GET")else ""
        self.queryparam = request["queryparam"] if "queryparam" in req_keys else ""


        # Initialize the response
        self.response = context["response"] if "response" in context.keys() else None
        if self.response is not None :
            self.status = self.response["status"]
            self.header = self.response["header"]
            self.body = self.response["body"]

    def get_data(self) -> dict:
        return {
            "method": self.method,
            "url": self.url,
            "path":self.path,
            "payload": self.payload,
            "queryparam": self.queryparam
        }
    def set_path(self,path: str):
        if not(path.startswith("/")):
            self.path = "/" + path
        else:
            self.path = path
        return True


    #send the request using all information
    def send(self) -> str:
        # TO DO : we can change it using client, to get more complexity
        response_result = ""
        url = self.url + (self.path if self.path != None else "")

        match self.method:
            case "GET":
                response_result=httpx.get(
                    url= url,
                    headers=self.header,
                    params=self.queryparam
                )
            case "POST":
                response_result=httpx.post(
                    url= url,
                    headers=self.header,
                    params=self.queryparam,
                    data=self.payload
                )
                pass
            case "PUT":
                response_result = httpx.put(
                    url=url,
                    headers=self.header,
                    params=self.queryparam,
                    data=self.payload
                )
            case "DELETE":
                response_result = httpx.delete(
                    url=url,
                    headers=self.header,
                    params=self.queryparam
                )
            case _:
                Exception("unknown method")

        return response_result