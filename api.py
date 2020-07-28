from flasgger import Swagger
from flask import Flask, jsonify, request
from nameko import config
from nameko.standalone.rpc import ClusterRpcProxy

from api_request_checks import (ArbitraryError400, CheckContentType,
                                CheckDataContent)

app = Flask(__name__)
Swagger(app)

conf = {
    'AMQP_URI': "pyamqp://user:password@localhost"
}
config.setup(conf)

@app.route('/health', methods=['GET'])
def health():
    """Returns a basic overview of system health TODO Expand this
    ---
    responses:
        200:
            description: The API server is healthy. Payload contains health of underlying services
    """

    health = dict(
        stream_service = False
    )

    with ClusterRpcProxy(conf) as rpc:
        health['stream_service'] = (rpc.stream_service.ping() == "pong")

        return health,200

@app.route('/stream', methods=['POST'])
def create():
    """Creates a new stream
    ---
    parameters:
        - in: body
          name: stream
          description: The stream to create
          schema:
            type: object
            required: true
            properties:
                url:
                    type: string
                    example: https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8
                    description: The streams master manifest
                name:
                    type: string
                    example: "Bitdash Sintel VOD Example"
                    description: The identifying name of the stream
                enabled:
                    type: boolean
                    example: false
                    description: Whether or not the stream is running checks
                tags:
                    type: array
                    description: List of tags for searching/categorization
                    example: ['sintel', 'akamai', 'vod']
                    items:
                        type: string
                polling_frequency:
                    description: Global frequency of runs for checks
                    example: 60
                    type: integer
    responses:
        201:
            description: A stream was successfully created TODO Expand this
        400:
            description: A malformed request was sent, did you set Content-Type?
        500:
            description: An internal error occured while processing the request
        
    """

    
    content_type = CheckContentType(request)
    if content_type is not None:
        return content_type

    if not request.is_json:
        return "not json?", 200 #TODO: Handle not json
    data = request.json

    with ClusterRpcProxy(conf) as rpc:
        result = rpc.stream_service.create(data)

        return result, 200

    


@app.route('/streams', methods=['GET'])
def page():
    """Returns a page of streams
    ---
    parameters:
      - name: next
        in: query
        required: false
        type: string
        description: Pagination token for next batch. From previous page. TODO Expand this
    responses:
        200:
            description: A page of streams represented by json
            schema:
                type: object
                properties:
                    data:
                        type: array
                        description: List of returned streams
                        items:
                            type: object
                            description: A stream object
                            properties:
                                _id:
                                    type: string
                                    example: 5f1d5d6f292c273f182b9f72
                                    description: String representation of the streams bson.ObjectId
                                url:
                                    type: string
                                    example: https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8
                                    description: The streams master manifest
                                name:
                                    type: string
                                    example: "Bitdash Sintel VOD Example"
                                    description: The identifying name of the stream
                                enabled:
                                    type: boolean
                                    example: false
                                    description: Whether or not the stream is running checks
                                tags:
                                    type: array
                                    description: List of tags for searching/categorization
                                    example: ['sintel', 'akamai', 'vod']
                                    items:
                                        type: string
                                polling_frequency:
                                    description: Global frequency of runs for checks
                                    example: 60
                                    type: integer
                                created_at:
                                    type: string
                    next:
                        type: string
                        example: "5f1d5d6f292c273f182b9f72"
                        description: Token for retrieving next page
            examples:
                application/json: |
                    {
                        "data": [{
                            "_id": {
                                "$oid": "5f1d5d6f292c273f182b9f72"
                            },
                            "enabled": true,
                            "name": "Streaming TV! Live",
                            "polling_frequency": 30,
                            "created_at": "2020-07-26 03:39:43.315395",
                            "tags": ["bitdash", "hls", "vod", "akamai"],
                            "url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
                        }, {
                            "_id": {
                                "$oid": "5f1d5d6f292c273f182b9f73"
                            },
                            "enabled": true,
                            "name": "Apple Sample",
                            "polling_frequency": 30,
                            "created_at": "2020-07-26 03:39:43.380649",
                            "tags": ["bipbopall", "hls", "apple"],
                            "url": "http://devimages.apple.com/iphone/samples/bipbop/bipbopall.m3u8"
                        }],
                        "next": "5f1d5d6f292c273f182b9f73"
                    }
    """
    args = request.args

    next_page = None
    if "next" in request.args:
        next_page = request.args.get("next")
    
    
    with ClusterRpcProxy(conf) as rpc:
        result = rpc.stream_service.page(next_page)
        return result

@app.route('/stream/<stream_id>', methods=['GET'])
def get(stream_id):
    """Returns a single stream
    ---
    parameters:
        - name: stream_id
          description: The id of the stream to request
          example: 5f1d5d6f292c273f182b9f72
          in: path
          type: string
          required: true
    responses:
        '200':
            description: A stream represented by json
            schema:
                type: object
                description: Stream parameters
                properties:
                    _id:
                        type: string
                        description: String representation of the streams bson.ObjectId
                    url:
                        type: string
                        example: https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8
                        description: The streams master manifest
                    name:
                        type: string
                        example: "Bitdash Sintel VOD Example"
                        description: The identifying name of the stream
                    enabled:
                        type: boolean
                        example: false
                        description: Whether or not the stream is running checks
                    tags:
                        type: array
                        description: List of tags for searching/categorization
                        example: ['sintel', 'akamai', 'vod']
                        items:
                            type: string
                    polling_frequency:
                        description: Global frequency of runs for checks
                        example: 60
                        type: integer
                    created_at:
                        type: string
            examples:
                application/json: |
                    {
                    "_id": "5f1d5d6f292c273f182b9f72",
                    "created_at": "2020-07-26 03:39:43.315395",
                    "enabled": true,
                    "name": "Streaming TV Live!",
                    "polling_frequency": 30,
                    "tags": [
                        "bitdash",
                        "blender",
                        "hls",
                        "vod"
                    ],
                    "url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
                    }
        404:
            description: Not found
    """
    
    #with ClusterRpcProxy(config={"AMQP_URI":"pyamqp://user:password@127.0.0.1"}) as rpc:
    with ClusterRpcProxy(conf) as rpc:
        result = rpc.stream_service.get(stream_id)
        return result, 200


@app.route('/stream/<stream_id>', methods=['PATCH'])
def patch(stream_id):
    """Updates a single stream
    ---
    responses:
        200:
            description: Success
    """
    return None,501

@app.route('/stream/<stream_id>', methods=['DELETE'])
def delete(stream_id):
    """Deletes the given stream
    ---
    responses:
        200:
            description: Delete success
    """
    return None,501

app.run(debug=True)
