# Mongo Backend
import hashlib

from bson.objectid import ObjectId
from nameko import config
from nameko.extensions import DependencyProvider
from nameko.rpc import rpc
from pymongo import MongoClient

MONGODB_URI_KEY = "MONGODB_CONNECTION_STRING"
PAGINATION_KEY = "MAX_PAGINATION"


class NotFound(Exception):
    pass

class StreamStorageWrapper:
    """
        MongoDB Interface Wrapper
    """

    NotFound = NotFound

    def __init__(self, client, db):
        self.client = client
        self.db = db
        self.collection = self.db.streams

    def _format_key(self, stream_id):
        return ObjectId(stream_id)

    def create(self, stream):
        r = self.collection.insert_one(stream).inserted_id
        return r
    
    def page(self, last):
        limit = config.get(PAGINATION_KEY)
        if last is None:
            chunk = self.collection.find().limit(limit)
        else:
            chunk = self.collection.find({'_id': {'$gt': ObjectId(last)}}).limit(limit)

        data = [x for x in chunk]

        if not data:
            return None, None
        
        last_id = str(data[-1]['_id'])
        return data, last_id

    def get(self, stream_id):
        stream = self.collection.find_one({"_id": self._format_key(stream_id)})
        return stream

class StreamStorage(DependencyProvider):

    def setup(self):
        self.client = MongoClient(config.get(MONGODB_URI_KEY))
        self.db = self.client.streams
    
    def get_dependency(self, worker_ctx):
        return StreamStorageWrapper(self.client, self.db)






"""
    def new_prompt(self, filename, col, text):
        h = hashlib.md5(text)

        exists = self.get_prompt_by_hash({'md5': h})
        if (exists is not None):
            return exists

        d = {
            'originating_column': [col],
            'originating_file': [filename],
            'text': [text],
            'md5': [h]
        }
        df = pd.DataFrame(d, index=[0])
        p = self.prompts()
        results = p.insert_many(df.to_dict("records"))
        return results



class Backend:
    '''The mongodb interface'''

    def __init__(self, connection_string, db):
        if connection_string == "":
            self.client = MongoClient(default_connection_string)
        else:
            self.client = MongoClient(connection_string)
    
        self.db = self.client[db]

    def create_stream(self):
        return None


class BackendService:
    '''The mongodb service'''
    name = 'backend_service'
    backend = Backend("", "praetor")

    @rpc
    def read(self):
        return "Testing"
"""
