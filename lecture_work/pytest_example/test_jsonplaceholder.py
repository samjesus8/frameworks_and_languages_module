import requests

ENDPOINT="https://jsonplaceholder.typicode.com/"

def test_get_post():
    response = requests.get(ENDPOINT + 'posts/1')
    assert response.status_code == 200

def test_create_post():
    ITEM={"title": "foo", "body": "bar", "userId": "1"}
    post = requests.post(ENDPOINT + 'posts', json=ITEM)
    data = post.json()
    assert data['id'] > 100

def test_delete_post():
    response = requests.delete(ENDPOINT + 'posts/1')
    assert response.status_code == 200