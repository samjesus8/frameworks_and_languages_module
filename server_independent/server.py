from wsgiref.simple_server import make_server
import falcon
from falcon_cors import CORS
import json
import datetime

# "pip install falcon-cors" in order to use this
# Enabling use of CORS middleware (OPTIONS request)
cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)

items = [  
    {
        "id": 3528640174782866,
        "user_id": "Sam1234",
        "keywords": [
            "Word1",
            "Word2",
            "Word3"
        ],
        "description": "111111111111",
        "image": "https://i.imgur.com/SCEwQdK.jpeg",
        "lat": 13.16937,
        "lon": -82.39787,
        "date_from": "2023-10-30T11:09:14.606Z",
        "date_to": "2023-10-30T11:09:14.606Z"
    }
]

class RootResource:
    def on_get(self, req, resp):
        try:
            # Serve the client.html file when accessing the root endpoint
            with open("client.html", "r") as file:
                resp.status = falcon.HTTP_200
                resp.content_type = "text/html"
                resp.text = file.read()
        except FileNotFoundError:
            # If it cannot find client.html then return 404
            resp.status = falcon.HTTP_404
            resp.text = "File not found"
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.text = f"Internal Server Error: {str(e)}"

    def on_options(self, req, resp):
        # Respond to CORS requests
        resp.status = falcon.HTTP_204
        resp.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

class CreateItemResource:
    def on_post(self, req, resp):
        # Parse the JSON payload from the request body
        req_data = json.loads(req.bounded_stream.read().decode('utf-8'))

        if req_data.get("user_id") is None or req_data.get("keywords") is None or req_data.get("description") is None or req_data.get("lat") is None or req_data.get("lon") is None:
            resp.status = falcon.HTTP_405
            resp.media = "Invalid input - some input fields may be missing"
            return
        else:
            # Generate missing details
            new_item = {
                'id': int(datetime.datetime.now().timestamp() * 1000000),  # 15-digit timestamp as an integer
                **req_data,
                'date_from': datetime.datetime.now().isoformat(), # Date in ISO format
                'date_to': datetime.datetime.now().isoformat(),
            }

            # Add item to the list
            items.append(new_item)

            # Return 201 and the JSON data
            resp.status = falcon.HTTP_201
            resp.media = new_item

class ItemsResource:
    def on_get(self, req, resp, item_id):
        item_id = int(item_id)

        for i in items:
            if i['id'] == item_id:
                resp.media = i
                resp.status = falcon.HTTP_200
                break
            else:
                resp.media = {'error': 'Item not found'}
                resp.status = falcon.HTTP_404
    
    def on_delete(self, req, resp, item_id):
        # Parse the ID parameter
        id = int(item_id)
        itemIndex = None

        for index, item in enumerate(items):
            if item['id'] == id:
                itemIndex = index
                break


        # Check if the item was found
        if itemIndex == None:
            resp.status = falcon.HTTP_404 # Return 404 if no item was found
            resp.text = "Item not found"
        else:
            # Delete the item from the ITEMS array
            items.pop(itemIndex)

            # Respond with a 204 status code indicating a successful deletion
            resp.status = falcon.HTTP_204

class GetItemsResource:
    def on_options(self, req, resp):
        # Respond to CORS requests
        resp.set_header('Access-Control-Allow-Origin', '*')

    def on_get(self, req, resp): ## Handles GET /items
        resp.media = items
        resp.status = falcon.HTTP_200

app = falcon.App(middleware=[cors.middleware])  # Instantiate App with CORS middleware

# ENDPOINTS
app.add_route("/", RootResource())
app.add_route('/items', GetItemsResource())
app.add_route("/item/{item_id}", ItemsResource())
app.add_route("/item", CreateItemResource())
#app.add_route("/item/{item_id}", delete_item, methods=['DELETE'])

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server shutting down...")