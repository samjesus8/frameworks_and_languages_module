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

app.get('/', (req, res) => {
  res.status(200).sendFile("/workspaces/frameworks_and_languages_module/client/client.html");
})

app.get('/items', (req, res) => {
  console.log("GET 200");
  res.status(200).json(ITEMS);
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
  const expectedFields = ["user_id", "keywords", "description", "image", "lat", "lon"];
  
  // Check if all expected fields are present in the request body
  const allFieldsPresent = expectedFields.every(field => field in req.body);

  if (!allFieldsPresent) {
    console.log("POST 405 - Missing Fields");
    console.log(req.body);
    return res.status(405).json({"message": "missing fields"});
  }

  //Check if the JSON is in the correct format
  if (
    typeof req.body.user_id !== 'string' ||
    !Array.isArray(req.body.keywords) || !req.body.keywords.every(keyword => typeof keyword === 'string') ||
    typeof req.body.description !== 'string' ||
    typeof req.body.image !== 'string' ||
    typeof req.body.lat !== 'number' || isNaN(req.body.lat) ||
    typeof req.body.lon !== 'number' || isNaN(req.body.lon)
  ) {
    console.log("POST 405 - Invalid Input Structure");
    console.log(req.body);
    return res.status(405).json({"message": "Invalid Input Structure"});
  }

  //If all checks are correct, generate any missing details
  let newItem = {
    ...req.body,
    // Generate 'id'
    id: Math.floor(Math.random() * Number.MAX_SAFE_INTEGER),

    // Generate 'date_from' and 'date_to' (using the current date)
    date_from: new Date().toISOString(),
    date_to: new Date().toISOString()
  };

  //Add item to list and complete
  ITEMS.push(newItem);
  console.log("POST 201 - Item Created");
  res.status(201).json(newItem);
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
  console.log("DELETE 204 id: " + itemID.toString());
  res.status(204).json();
})

app.listen(port, () => {
  console.log(`Samuel Jesuthas Assignment listening on port ${port}`);
})

process.on('SIGINT', function() {process.exit()})