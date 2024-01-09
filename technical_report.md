Technical Report
================

This report endeavors to delve into great detail on programming frameworks and languages and their importance in addressing programming-related challenges. To accomplish this objective, an examination of various features on both client and server aspects of Frameworks/Languages will be conducted. Furthermore, an in-depth analysis of an existing prototype will be undertaken, aiming to identify potential shortcomings and ascertain its compatibility within a corporate environment.

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


What is ... (1978) Amazon. Available at: https://aws.amazon.com/what-is/middleware/ (Accessed: 24 December 2023).

Middleware. Available at: https://docs.djangoproject.com/en/5.0/topics/http/middleware/ (Accessed: 24 December 2023). 

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

Flask Tutorial: Routes (no date) Flask Tutorial: Routes - Python Tutorial. Available at: https://pythonbasics.org/flask-tutorial-routes/ (Accessed: 25 December 2023).

### Request/Response Handling and Serialization

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

WSGI Request & Response - Falcon 3.1.3 documentation. Available at: https://falcon.readthedocs.io/en/3.1.3/api/request_and_response_wsgi.html (Accessed: 25 December 2023). 

Server Language Features
-----------------------

### Asynchronous Programming in Python

- This feature in python is provided by the `asyncio` library, which allows non-blocking execution of tasks. Running a program asynchronously usually increases the performance of the program, however it is down to the developer to ensure each event is managed properly
- This is a simple async implementation in python, which just prints "start" and then waits for 2 seconds before printing "end"

    ```python
    import asyncio

    async def async_example():
        print("Start")
        await asyncio.sleep(2)
        print("End")

    asyncio.run(async_example())
    ```

- Asynchronous programming enhances server efficiency by enabling concurrent execution of multiple tasks, preventing blocking operations, and improving overall responsiveness in applications with high I/O operations.

Asyncio - asynchronous I/O Python documentation. Available at: https://docs.python.org/3/library/asyncio.html (Accessed: 04 January 2024). 


### Typescript in Node.js

- Typescript is actually a superset of JavaScript, which provides static typing for Node.js
- This feature allows you to be able to catch potential errors during development, enhance the readability of your code, and overall improves the maintainability of your server

    ```typescript
    interface User {
    id: number;
    username: string;
    }

    function getUserInfo(user: User): string {
    return `ID: ${user.id}, Username: ${user.username}`;
    }
    ```

- The main benefits of this feature is that it heavily reduces debugging & development time, as it helps catch type-related errors early in the development process, which in return makes your code more robust.

Documentation - typescript for JavaScript programmers TypeScript. Available at: https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html (Accessed: 04 January 2024). 

Client Framework Features
-------------------------

### React Hooks for State Management

- React Hooks, like `useState` and `useEffect`, enable functional components to manage state and side effects. They streamline code by replacing class-based components, providing a more concise and readable structure.

  ```javascript
  import React, { useState, useEffect } from 'react';

  function ExampleComponent() {
    const [count, setCount] = useState(0);

    useEffect(() => {
      document.title = `Count: ${count}`;
    }, [count]);

    return (
      <div>
        <p>You clicked {count} times</p>
        <button onClick={() => setCount(count + 1)}>
          Click me
        </button>
      </div>
    );
  }
  ```

- React Hooks simplify state management and side effect handling in functional components, making code more readable, reducing boilerplate, and enhancing the overall developer experience.

Built-in react hooks. Available at: https://react.dev/reference/react/hooks (Accessed: 04 January 2024). 


### Vue.js Single File Components

- Vue.js Single File Components encapsulates a component's template, script, and styles in one single file. This organized structure enhances readability, maintainability, and allows for better component-based development.

  ```html
  <template>
    <div>
      <h1>{{ message }}</h1>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        message: 'Hello, Vue!'
      };
    }
  }
  </script>

  <style scoped>
  h1 {
    color: blue;
  }
  </style>
  ```

- You can see this is a HTML file, however we have the main HTML boilerplate, a script, and a CSS stylesheet all in the same file. Therefore reducing the amount of individual JS or CSS files you have to work with
- This simplifies your overall code and it allows for certain parts of your code to be reusable, making this a cleaner and more maintainable client project

Vue.js Single-File Components | Vue.js. Available at: https://vuejs.org/guide/scaling-up/sfc.html (Accessed: 04 January 2024). 

### Angular Dependency Injection

- Angular's Dependency Injection system allows components and services to request dependencies rather than creating them. This promotes modular and testable code by facilitating the management of component dependencies.

  ```javascript
  import { Component } from '@angular/core';

  @Injectable()
  class DataService {
    getData() {
      // Fetch data logic
    }
  }

  @Component({
    selector: 'app-example',
    template: '<p>{{ data }}</p>'
  })
  export class ExampleComponent {
    constructor(private dataService: DataService) {
      this.data = this.dataService.getData();
    }
  }
  ```

- Dependency Injection is built-in for Angular. When a dependency is requested, the Injector checks its database to see if there is an existing instance available. This is what the `Injectable` attribute is for, which shows that a class can be injected via DI.
- This promotes code modularity, reusability, and testability by providing a centralized way to manage and inject dependencies into components and services.

Angular | Understanding dependency injection (no date) Angular. Available at: https://angular.io/guide/dependency-injection (Accessed: 04 January 2024). 

Client Language Features
------------------------

### JavaScript Arrow Functions

- This feature allows you to simplify a lot of code by providing a shorter syntax for certain functions, which are more implicit
- In this Javascript Example, you can see a simple function which adds 2 numbers together
  ```javascript
  // Traditional function
  function add(a, b) {
    return a + b;
  }

  // Arrow function
  const addArrow = (a, b) => a + b;
  ```
  - The arrow function simplifies the entire `add()` function into one line by using the `=>` syntax. 
  - We are basically saying for a temporary set of parameters called `(a, b)`, perform the following function which is `a + b`, and we are then storing it in a variable
- This feature reduces the amount of code you write by a lot in big projects, and it improves the overall readability of your code, which is a huge benefit to developers

MozDevNet Arrow function expressions - javascript: MDN, MDN Web Docs. Available at: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions (Accessed: 08 January 2024). 

### Enums in TypeScript

- A great tool to use in TypeScript is enums, which are very useful for declaring a custom set of constant values, which makes the different values easier to access in code
- You can see this in the below example, where a simple Direction enum is being declared
  ```typescript
    enum Direction {
    Up = 'UP',
    Down = 'DOWN',
    Left = 'LEFT',
    Right = 'RIGHT'
  }

  let playerDirection: Direction = Direction.Up;
  ```
  - We have declared custom variables for each direction like Up, Down etc. And we can use this enum to clearly access the constant you need. This helps reduce a lot of duplicated code and it's easier to maintain because enums are a clear, structured way to represent constants

  Handbook - enums (no date) TypeScript. Available at: https://www.typescriptlang.org/docs/handbook/enums.html (Accessed: 08 January 2024). 

Conclusion
-----------

Frameworks play a pivotal role in modern software development, offering developers a structured and efficient approach to building robust applications. They provide a foundation of pre-built components, tools, accelerating development and ensuring best developer practices. Frameworks streamline repetitive tasks, enhance code organization, and improve collaboration within development teams. The abstraction of common functionalities allows developers to focus on application-specific logic, increasing productivity and reducing development time. Moreover, frameworks often come with active communities, extensive documentation, and ongoing support, contributing to long-term project sustainability and maintenance. In a rapidly evolving technological landscape, leveraging frameworks is not just recommended but essential for achieving scalability, maintainability, and staying current with industry standards.

When selecting frameworks, it's crucial to align choices with project requirements, team expertise, and long-term goals. For server-side development, Node.js with Express is a popular choice due to its scalability and flexibility. React, Vue.js, and Angular stand out in the client-side domain, offering diverse solutions based on project size and complexity. TypeScript, with its static typing, can enhance development in both server and client frameworks, ensuring code reliability. The main thing, is to strike a balance between familiarity, community support, and alignment with project needs. Regularly adapting framework choices based on evolving project requirements and industry trends ensures the development of maintainable, scalable, and future-proof applications.