# Independent Client Framework - React

- This is an implementation of a React client-side application which is an optional requirement to pass this assignment
- In this `/independent_client` folder, there will be a working implementation of a React client-side application

## How to Run

1. Install axios to ensure React can handle HTTP requests
    ```
    $ npm install axios
    ```
2. Then run the application using `npm`
    ```
    $ npm start
    ```
3. Link with the server using `?api=` in your browser
    ```
    http://client:3000/?api=http://server:8000
    ```

## Running in Docker

You can also run this client in a Docker container. Here are some methods to get you up and running

### Manual Build/Run

1. Make sure you are in the `.../client/independent_client` directory
    ```
    $ cd client/independent_client
    ```
2. Using the Dockerfile, build your container
    ```
    $ docker build -t name-of-container .
    ```
3. Once the container has successfully built, run the container
    ```
    $ docker run -p 8001:8001 name-of-container
    ```

### Makefile

1. Again make sure you are in the `.../client/independent_client` directory

2. Now using the `Makefile`, you can build and run the Docker container at once by doing
    ```
    $ make build run
    ```