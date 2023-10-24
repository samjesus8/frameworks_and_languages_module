const express = require('express')
const app = express()
const port = 8000
const cors = require('cors')

app.use(express.json());
app.use(cors())

let ITEMS = [

]

app.get('/', (req, res) => {
  res.sendFile("client.html", {root: __dirname})
})

app.get('/items', (req, res) => {
  console.log("GET 200")
  res.json(ITEMS)
})

app.get('/item/:itemId', (req, res) => {
  const itemId = parseFloat(req.params.itemId); // Parse the ID parameter

  // Find the item with the specified ID
  const item = ITEMS.find(item => item.itemId === itemId);

  // Check if the item was found
  if (!item) {
    console.log("GET /item/{itemId} 404 itemId: " + itemId);
    return res.status(404).json({ message: 'Item not found' });
  }

  // Respond with a 200 status code and the specific item in valid JSON format
  console.log("GET /item/{itemId} 200")
  res.status(200).json(item);
})

app.post('/item', (req, res) => {
  if (Object.keys(req.body).sort().toString() != "description,image,itemId,keywords,lat,lon,user_id"){
    console.log("POST 405");
    console.log(req.body);
    return res.status(405).json({"message": "missing fields"})
  }
  ITEMS.push(req.body)
  console.log("POST 201")
  res.status(201).json()
})

app.delete('/item/:itemId', (req, res) => {
  const itemId = parseFloat(req.params.itemId); // Parse the ID parameter

  // Find the index of the item with the specified ID
  const itemIndex = ITEMS.findIndex(item => item.itemId === itemId);

  // Check if the item was found
  if (itemIndex === -1) {
    return res.status(404).json({ message: 'Item not found' });
  }

  // Delete the item from the ITEMS array
  ITEMS.splice(itemIndex, 1);

  // Respond with a 204 status code indicating a successful deletion
  console.log("DELETE 204 itemId: " + itemId);
  res.status(204).json();
})

app.listen(port, () => {
  console.log(`Samuel Jesuthas Assignment listening on port ${port}`)
})

process.on('SIGINT', function() {process.exit()})