import datetime

from bson.json_util import dumps, loads
from nameko.rpc import RpcProxy, rpc

import mongo
from stream_schema import Stream


class StreamService:
    name = "stream_service"

    storage = mongo.StreamStorage()

    @rpc
    def hello(self, test):
        return "Hello, {}!".format(test)
    
    @rpc
    def get(self, stream_id):
        r = self.storage.get(stream_id)
        return Stream().dump(r)
    
    @rpc
    def page(self, last=None):
        """Returns a paged list of streams
        ---
        parameters:
            - name: last
            in: path
            type: string
            required: false
            description: The pagination token for the next page
        responses:
            200:
                description: A list of streams
        """
        d, lastid = self.storage.page(last)

        response = dict(
            data=d,
            next=lastid
        )

        return dumps(response)

    @rpc
    def create(self, stream):
        stream.update(created_at = str(datetime.datetime.now()))
        s = Stream().load(stream)
        r = self.storage.create(s)
        resp = self.get(r)
        
        return Stream().dump(resp)

#class CheckService:
