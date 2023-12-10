# Client - Vue.js
- This is an implementation of an Vue.js client-side application which is a requirement to pass this assignment
- In this `/client` folder, there is a working implementation of a webpage which will be served via the server

## Steps to run

1. Make sure you have your server running in `/server`
    ```
    node server.js
    ```
2. Then serve the client page on port 8001 using Python's `http.server` function

    ```
    python -m http.server 8001
    ```

3. Open up the client page and then connect the client to the server by using the `?api=` term in your browser

    ```
    http://127.0.0.1:8001/?api=http://127.0.0.1:8000/
    ```
    ```
    http://client:8001/?api=http://server:8000
    ```

What this will do is connect the client to the server and you should be able to view any existing items

You can also add/delete items using the input boxes and buttons