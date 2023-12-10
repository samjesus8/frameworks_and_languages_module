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