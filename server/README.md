# Server - ExpressJS

- This is an implementation of an ExpressJS web-server which is a requirement to pass this assignment
- In this `/server` folder, there will be a working implementation of a Express web server, according to the `openapi.yaml` specification

# Steps to Run

## Run Locally
You can run this server in your code-spaces environment, or locally if you have cloned this repo

1. Install Express
    ```
    $ npm install express
    ```

2. Then run the `server.js` file by using `node`
    ```
    $ node server.js
    ```

## Run using Docker

You can use Docker to run this server in a container. Here are some ways to do this:

### Manual Build/Run

1. Make sure you are in the `.../server` directory
    ```
    $ cd server
    ```

2. Then build your Docker container by doing the following command

    ```
    $ docker build -t name-of-container .
    ```

3. Once it has successfully built, run the container using the following command

    ```
    $ docker run -p 8000:8000 name-of-container
    ```

### Makefile

You can build/run the container all at once by doing
```
$ make build run
```