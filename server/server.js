const express = require('express')
const app = express()
const port = 8000
const cors = require('cors')

app.use(express.json());
app.use(cors())

let ITEMS = [
  {
    "id": 3528640174782866,
    "user_id": "Sam1234",
    "keywords": [
      "Word1",
      " Word2",
      " Word3"
    ],
    "description": "111111111111",
    "image": "https://i.imgur.com/SCEwQdK.jpeg",
    "lat": "13.16937",
    "lon": "-82.39787",
    "date_from": "2023-10-30T11:09:14.606Z",
    "date_to": "2023-10-30T11:09:14.606Z"
  }
]

app.get('/', (req, res) => {
  res.sendFile("client.html", {root: __dirname})
})

app.get('/items', (req, res) => {
  console.log("GET 200");
  res.json(ITEMS)
})

app.get('/item/:itemId', (req, res) => {
  const itemId = parseFloat(req.params.id); // Parse the ID parameter

  // Find the item with the specified ID
  const item = ITEMS.find(item => item.id === itemId);

  // Check if the item was found
  if (!item) {
    console.log("GET /item/{itemId} 404 id: " + itemId);
    return res.status(404).json({ message: 'Item not found' });
  }

  // Respond with a 200 status code and the specific item in valid JSON format
  console.log("GET /item/{itemId} 200");
  res.status(200).json(item);
})

app.post('/item', (req, res) => {
  if (Object.keys(req.body).sort().toString() != "date_from,date_to,description,id,image,keywords,lat,lon,user_id"){
    console.log("POST 405");
    console.log(req.body);
    return res.status(405).json({"message": "missing fields"})
  }
  ITEMS.push(req.body)
  console.log("POST 201");
  res.status(201).json()
})

app.delete('/item/:itemId', (req, res) => {
  const itemID = parseFloat(req.params.id); // Parse the ID parameter

  // Find the index of the item with the specified ID
  const itemIndex = ITEMS.findIndex(item => item.id === itemID);

  // Check if the item was found
  if (itemIndex === 0) {
    return res.status(404).json({ message: 'Item not found' });
  }

  // Delete the item from the ITEMS array
  ITEMS.splice(itemIndex, 1);

  // Respond with a 204 status code indicating a successful deletion
  console.log("DELETE 204 id: " + itemID);
  res.status(204).json();
})

app.listen(port, () => {
  console.log(`Samuel Jesuthas Assignment listening on port ${port}`);
})

process.on('SIGINT', function() {process.exit()})