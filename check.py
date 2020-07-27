#from stream_schema import Stream
import urllib

import requests
from nameko.rpc import RpcProxy, rpc


class CheckService:
    name = "check_service"

    @rpc
    def ping(self):
        return "pong"

    @rpc
    def HTTPStatusOk(self, url):
        """Checks that a stream URL is accessible"""
        r = requests.head(url,allow_redirects=True,verify=False)
        return r.status_code




#class CheckInterface:
#
#    def __init__(self,stream_id):
#        self.stream = stream_id
#
#    def run():
#        print("Running check")

#def GetStatus(url):
#    #r = urllib.urlopen(url).getcode()
#    r = requests.head(url,allow_redirects=True)
#    return r.status_code
