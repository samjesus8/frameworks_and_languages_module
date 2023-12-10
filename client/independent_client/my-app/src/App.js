import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ItemList from './components/ItemList';
import CreateItemForm from './components/CreateItemForm';

const App = () => {
  const [items, setItems] = useState([]);

  const updateItems = () => {
    axios.get('/api/v1/items')
      .then(response => setItems(response.data))
      .catch(error => console.error(error));
  };

  const addItem = (newItem) => {
    axios.post('/api/v1/item', newItem)
      .then(() => {
        updateItems();
      })
      .catch(error => console.error(error));
  };

  const deleteItem = (itemId) => {
    axios.delete(`/api/v1/item/${itemId}`)
      .then(() => {
        updateItems();
      })
      .catch(error => console.error(error));
  };

  useEffect(() => {
    updateItems();
  }, []);

  return (
    <div>
      <h1>FreeCycle your old stuff - keep things out of landfill</h1>

      <h2>
        <ul>
          <li>Help the poor</li>
          <li>Climate crisis</li>
          <li>Right to repair</li>
        </ul>
      </h2>

      <div>
        <h2>Create</h2>
        <CreateItemForm onSubmit={addItem} />

        <h2>Items</h2>
        <ItemList items={items} onDelete={deleteItem} />
      </div>
    </div>
  );
};

export default App;