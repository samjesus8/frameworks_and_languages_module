# Independent Server Framework - Falcon

- This folder contains a working implementation of a different server framework compared to the original which is using express.js
- I will be using the **Falcon** framework to design and run a web server

## How to run

1. Ensure you have the latest version of Python installed
    ```
    apt-get install python
    ```

2. Ensure you have the necessary packages to run the server
    - Install falcon
        ```
        pip install falcon
        ```
    - Install falcon-cors
        ```
        pip install falcon-cors
        ```
    - You can also install both at once by doing
        ```
        pip install falcon falcon-cors
        ```

3. Then run the `server.py` file by doing
    ```
    python server.py
    ```
    You can also run the server by doing
    ```
    make run_local
    ```

## Running using Docker

You can run this server in a Docker Container. Here are some ways to get you up and running

### Manual Build/Run

1. Make sure you are in the `.../server/independent_server` directory

2. Then build your Docker container by doing the following command

    ```
    docker build -t name-of-container .
    ```

3. Once it has successfully built, run the container using the following command

    ```
    docker run -p 8000:8000 name-of-container
    ```

### Makefile

You can build & run your docker container at once by using the following command

```
make build run
```