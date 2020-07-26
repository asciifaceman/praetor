#from stream_schema import Stream
import urllib

import requests

#class CheckInterface:
#
#    def __init__(self,stream_id):
#        self.stream = stream_id
#
#    def run():
#        print("Running check")

def GetStatus(url):
    #r = urllib.urlopen(url).getcode()
    r = requests.head(url,allow_redirects=True)
    return r.status_code
