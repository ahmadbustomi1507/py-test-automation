import httpx

dict_base_header = {
    "Content-Type":"application/json",
    "Accept":"*/*"
}
class RestApiBuilder(object):
    def __init__(self,base_url):
        self.base_url = base_url
        self.header   = dict_base_header
        self.payload  = {}
        self.endpoint = ""
        self.resource = ""
        self.queryparam= ""

    def set_header(self,new_header):
        self.header[new_header]
        return True

    def set_payload(self,new_payload):
        self.payload = new_payload

    def set_endpoint(self,endpoint):
        self.endpoint = endpoint
        self.__set_resource()

    # def set_pathparam(self,new_pathparam):
    #     self.pathparam = new_pathparam

    # qquery param of a dictionary or tuple
    def set_query_param(self,new_queryparam):
        self.queryparam = new_queryparam

    # httpx will provide better approach rather than
    # joining manually
    def __set_resource(self):

        self.resource = ''.join([
            self.base_url,
            self.endpoint
        ])


    # send request GET and POST
    def send_post_request(self,payload):
        self.__set_resource()
        return httpx.post(self.resource,
                          data=self.payload,
                          params=self.queryparam)

    def send_get_request(self):
        self.__set_resource()
        print(f"resource {self.resource}")
        return httpx.get(self.resource,
                          params=self.queryparam)

