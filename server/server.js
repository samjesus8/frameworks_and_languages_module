const express = require('express')
const app = express()
const port = 8000
const cors = require('cors')

app.use(express.json());
app.use(cors())

let ATTENDEES = [

]

app.get('/', (req, res) => {
  res.sendFile("client.html", {root: __dirname})
})

app.get('/attendees', (req, res) => {
  res.json(ATTENDEES)
})

app.post('/attendee', (req, res) => {
  if (Object.keys(req.body).sort().toString() != "id,name,notes"){
    return res.status(405).json({"message": "missing fields"})
  }
  ATTENDEES.push(req.body)
  res.status(201).json()
})

app.delete('/attendee/:id', (req, res) => {
  const id = parseFloat(req.params.id)
  ATTENDEES = ATTENDEES.filter(attendee => attendee.id != id)
  res.status(204).json()
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

process.on('SIGINT', function() {process.exit()})