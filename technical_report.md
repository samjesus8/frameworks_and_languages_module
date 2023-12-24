Technical Report
================

This report endeavors to delve into the intricacies of programming frameworks and languages, their significance, and their utility in addressing programming-related challenges. To accomplish this objective, an examination of various features on both client and server aspects of Frameworks/Languages will be conducted. Furthermore, an in-depth analysis of an existing prototype will be undertaken, aiming to identify potential shortcomings and ascertain its compatibility within a corporate environment.

Critique of Server/Client prototype
---------------------

### Overview

### CORS Default Parameter

`./example_server/app/http_server.py`
```python
RESPONSE_DEFAULTS = {
    'code': 200, 
    'body': '',
    'Content-type': 'text/html; charset=utf-8',
    'Server': 'CustomHTTP/0.0 Python/3.9.0+',
    'Access-Control-Allow-Origin': '*'
}
```

These are the default responses set on this web-server unless it has been specified/overridden elsewhere. The `Access-Control-Allow-Origin` has been set by default to allow outside domains to access our server, which makes this server vulnerable to possible security related issues

### Lack of Middleware

- The lack of middleware is evident in the absence of a modular component responsible for processing requests before they reach the main application logic
- This can be seen in the `serve_app` function in the `http_server.py` file, where this method is directly handling the request without doing any middleware processing. A middleware layer could be added between receiving the request and invoking the main application, allowing for more flexibility and separation of concerns.

```python
def serve_app(func_app, port, host=''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        while True:
            s.listen()
            try:
                conn, addr = s.accept()
            except KeyboardInterrupt as ex:
                break
            with conn:
                #log.debug(f'Connected by ')
                #while True:
                    data = conn.recv(65535)  # If the request does not come though in a single recv/packet then this server will fail and will not composit multiple TCP packets. Sometimes the head and the body are sent in sequential packets. This happens when the system switches task under load.
                    #if not data: break
                    try:
                        request = parse_request(data)
                    except InvalidHTTPRequest as ex:
                        log.exception("InvalidHTTPRequest")
                        continue

                    # HACK: If we don't have a complete message - try to botch another recv - I feel dirty doing this 
                    # This probably wont work because utf8 decoded data will have a different content length 
                    # This needs more testing
                    while int(request.get('content-length', 0)) > len(request['body']):
                        request['body'] += conn.recv(65535).decode('utf8')

                    try:
                        response = func_app(request)
                    except Exception as ex:
                        log.error(request)
                        traceback.print_exc()
                        response = {'code': 500, 'body': f'<PRE>{traceback.format_exc()}</PRE>'}
                    # TODO: the code and content length do not work here - they are currently applied in encode response.
                    log.info(f"{addr} - {request.get('path')} - {response.get('code')} {response.get('Content-length')}")
                    conn.send(encode_response(response))
```

- This absence of middleware can lead to challenges in maintaining and extending the server, as modifications or additions to request processing logic would need to be directly implemented in the main application code.

### Recommendation

- The existing implementation lacks a middleware layer, which reduces modularity and maintainability. This can lead to challenges in extending functionality and handling diverse request processing requirements. Changing to established frameworks, like Flask or Django, would offer built-in middleware support, allowing scalable and maintainable server development.


Server Framework Features
-------------------------

### Built-in Middleware support

- Middleware in a server model, allows the ability to do pre/post processing on a request before it gets to the output. This can involve things like authentication, JSON request parsing and even logging
- This is an example of middleware implementation in Django:

```python
# Middleware class example in Django
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Custom middleware before view is called
        response = self.get_response(request)
        # Return the response after it has been processed by the middleware
        return response
```
- The reason middleware is so important is because it allows a structured way to process requests, which improves the modularity and ease to work on the server code. This solves the problem of the communication between different frameworks, without having to modify the main logic, or hardcode lots of logic into the main code due to the lack of middleware

    - [Django Middleware documentation](https://docs.djangoproject.com/en/5.0/topics/http/middleware/)
    - [AWS - What is middleware?](https://aws.amazon.com/what-is/middleware/)

### Routing and URL Mapping

- Server frameworks allow easy organization of endpoints. In a business environment, a server may have several hundreds of endpoints and it would be cumbersome to manually code in every single URL that is possible in your website.
- You can see in this Flask Example, it is very simple to create an endpoint and assign a method/function to it:

```python
# Routing example in Flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'
```
- You can add multiple endpoints by using the `@app.route()` attribute, which improves the manageability of this server
- Routing simplifies the organization of code by associating specific functions or handlers with defined endpoints. This improves the readability, scalability, and efficient request handling.
    - [Flask Routing](https://pythonbasics.org/flask-tutorial-routes/)

### Request/Response Handling and Serialization

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)

- A good feature of server frameworks is the built-in ability to handle incoming web requests. They also have the ability to handle data, and serializing request bodies so that it is inline with the API specification
- We can see this in this Falcon example:

```python
# Request handling and response serialization in Falcon
import falcon
import json

class Resource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'message': 'Hello, Falcon!'})

app = falcon.App()
app.add_route('/hello', Resource())
```

- What we are doing is assigning the Class `Resource` to the endpoint `/hello`. And in this class, is a function for handling a simple `GET` request. The method returns `200` as the status code and it returns a JSON body with a simple message `Hello, Falcon!`
- Built-in request/response handling simplifies developers' tasks which reduces boilerplate code. Frameworks often provide serializers for converting complex data types to and from formats like JSON, enhancing ease of use.
    - [Falcon Request Handling](https://falcon.readthedocs.io/en/3.1.3/api/request_and_response_wsgi.html)

Server Language Features
-----------------------

### (name of Feature 1)

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)


### (name of Feature 2)

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)



Client Framework Features
-------------------------

### (name of Feature 1)

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)


### (name of Feature 2)

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)


### (name of Feature 3)

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)


Client Language Features
------------------------

### (name of Feature 1)

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)

### (name of Feature 2)

(Technical description of the feature - 40ish words)
(A code block snippet example demonstrating the feature)
(Explain the problem-this-is-solving/why/benefits/problems - 40ish words)
(Provide reference urls to your sources of information about the feature - required)



Conclusions
-----------

(justify why frameworks are recommended - 120ish words)
(justify which frameworks should be used and why 180ish words)
