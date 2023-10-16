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
  res.json(ITEMS)
})

// To be implemented. Get a specific item
//app.get('/item', (req, res) => {})

app.post('/item', (req, res) => {
  console.log("POST FUNCTION")
  if (Object.keys(req.body).sort().toString() != "id,user_id,keywords,description,image,lat,lon,date_from,date_to"){
    return res.status(405).json({"message": "missing fields"})
  }
  ITEMS.push(req.body)
  res.status(201).json()
})

app.delete('/item/:itemId', (req, res) => {
  const id = parseFloat(req.params.id)
  ITEMS = ITEMS.filter(attendee => attendee.id != id)
  res.status(204).json()
})

app.listen(port, () => {
  console.log(`Samuel Jesuthas Assignment listening on port ${port}`)
})

process.on('SIGINT', function() {process.exit()})