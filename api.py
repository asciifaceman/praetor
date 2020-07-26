from flasgger import Swagger
from flask import Flask, jsonify, request
from nameko import config
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)

conf = {
    'AMQP_URI': "pyamqp://user:password@localhost"
}
config.setup(conf)

@app.route('/stream', methods=['POST'])
def create():
    """Creates a new stream
    ---
    responses:
        200:
            description: A stream was successfully created
    """

    print("not")
    return "",200

@app.route('/streams', methods=['GET'])
def page():
    """Returns a page of streams
    ---
    parameters:
      - name: next
        in: query
        required: false 
        type: string
        description: Pagination token for next batch. From previous page.
    responses:
        200:
            description: A page of streams represented by json
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
          in: path
          type: string
          required: true
    responses:
        200:
            description: A stream represented by json
    """
    
    #with ClusterRpcProxy(config={"AMQP_URI":"pyamqp://user:password@127.0.0.1"}) as rpc:
    with ClusterRpcProxy(conf) as rpc:
        result = rpc.stream_service.get(stream_id)
        return result, 200

app.run(debug=True)
