from wsgiref.simple_server import make_server
import falcon
from falcon_cors import CORS
import json
from datetime import datetime

# "pip install falcon-cors" in order to use this
# Enabling use of CORS middleware (OPTIONS request)
cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)

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
        resp.set_header('Allow', 'GET, OPTIONS')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        resp.set_header('Access-Control-Allow-Headers', '*')

class ItemsResource:
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

    def on_get(self, req, resp): ## Handles GET /items
        resp.status = falcon.HTTP_200
        resp.text = json.dumps(self.items, indent=2)

    def get_item_by_id(self, item_id): ## Handles GET /item/{itemId}
        for item in ItemsResource.items:
            if item["id"] == item_id:
                return item
        return None

    def get_item_index_by_id(self, item_id):
        for i, item in enumerate(self.items):
            if item["id"] == item_id:
                return i
        return -1

class ItemResource:
    def on_get(self, req, resp, item_id):
        # Parse the ID parameter
        item_id = int(item_id)

        # Find the item with the specified ID
        item = items.get_item_by_id(item_id)
        if item:
            resp.status = falcon.HTTP_200
            resp.text = json.dumps(item, indent=2)
        else:
            resp.status = falcon.HTTP_404
            resp.text = "Item not found"

    def get_item_by_id(self, item_id): ## Handles GET /item/{itemId}
        for item in ItemsResource.items:
            if item["id"] == item_id:
                return item
        return None

class CreateItemResource:
    def on_post(self, req, resp):
        # Parse the JSON payload from the request body
        try:
            req_data = json.loads(req.bounded_stream.read().decode('utf-8'))
            print(req_data)
        except json.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.text = "Invalid JSON payload"
            return

        # Check if all expected fields are present in the request body and have valid non-empty values
        expected_fields = ['user_id', 'keywords', 'description', 'image', 'lat', 'lon']

        # If 'image' is provided, check for 6 fields; otherwise, stick to 5
        if 'image' in req_data:
            print(req_data)
        else:
            expected_fields.remove('image')

        if not all(field in req_data and req_data[field] for field in expected_fields):
            resp.status = falcon.HTTP_405
            resp.text = "Invalid input - some input fields may be missing"
            return

        # Generate missing details
        new_item = {
            'id': int(datetime.now().timestamp() * 1000000),  # 15-digit timestamp as an integer
            **req_data,
            'date_from': datetime.now().isoformat(), # Date in ISO format
            'date_to': datetime.now().isoformat(),
        }

        # Add item to the list
        ItemsResource.items.append(new_item)

        # Return 201 and the JSON data
        resp.status = falcon.HTTP_201
        resp.text = json.dumps(new_item, indent=2)

class DeleteItemResource:
    def on_delete(self, req, resp, item_id):
        # Parse the ID parameter
        item_id = int(item_id)

        # Find the index of the item with the specified ID
        item_index = items.get_item_index_by_id(item_id)

        # Check if the item was found
        if item_index == -1:
            resp.status = falcon.HTTP_404 # Return 404 if no item was found
            resp.text = "Item not found"
            return

        # Delete the item from the ITEMS array
        ItemsResource.items.pop(item_index)

        # Respond with a 204 status code indicating a successful deletion
        resp.status = falcon.HTTP_204

    def get_item_index_by_id(self, item_id):
        for i, item in enumerate(ItemsResource.items):
            if item["id"] == item_id:
                return i
        return -1

app = falcon.App(middleware=[cors.middleware])  # Instantiate App with CORS middleware

# Create instances of the resource classes
root = RootResource()
items = ItemsResource()
item = ItemResource()
create_item = CreateItemResource()
delete_item = DeleteItemResource()

# ENDPOINTS
app.add_route("/", root)
app.add_route('/items', items)
app.add_route("/item/{item_id}", item)
app.add_route("/item", create_item, methods=['POST'])
app.add_route("/item/{item_id}", delete_item, methods=['DELETE'])

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server shutting down...")