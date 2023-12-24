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
