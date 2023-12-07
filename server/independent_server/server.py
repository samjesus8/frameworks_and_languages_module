from wsgiref.simple_server import make_server
import falcon
from falcon_cors import CORS
import json

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
            resp.status = falcon.HTTP_404
            resp.text = "File not found"
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.text = f"Internal Server Error: {str(e)}"

    def on_options(self, req, resp):
        # Respond to CORS requests
        resp.status = falcon.HTTP_200
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


app = falcon.App(middleware=[cors.middleware])  # Instantiate App with CORS middleware

# Create instances of the resource classes
items = ItemsResource()
item = ItemResource()
root = RootResource()

# ENDPOINTS
app.add_route("/", root)
app.add_route('/items', items)
app.add_route("/item/{item_id}", item)

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server shutting down...")