from wsgiref.simple_server import make_server
import falcon
import json

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

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps(self.items, indent=2)

app = falcon.App()

# Resources are represented by long-lived class instances
items = ItemsResource()

# items will handle all requests to the '/items' URL path
app.add_route('/items', items)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()