from error_schema import Error400


def CheckContentType(request):
    if request.headers['Content-Type'] not in 'application/json':
        msg = dict(
            status = 400,
            error = "Content-Type must be application/json"
        )
        return Error400().load(msg), msg['error']

def CheckDataContent(data):
    if data == None:
        msg = dict(
            status = 400,
            error = "No body"
        )
        return Error400().load(msg), msg['error']

def ArbitraryError400(message):
    msg = dict(
        status = 400,
        error = message
    )
    return Error400().load(msg), msg['error']
