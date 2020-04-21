from flask import escape

def hello_user(request):
    try:
        request_arguments = request.args
        username = request_arguments['username']
        return f'Hello {username}!'
    except:
        return 'Hello World!'