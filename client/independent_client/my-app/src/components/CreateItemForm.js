import React, { useState } from 'react';

const CreateItemForm = ({ onSubmit }) => {
  const [newItem, setNewItem] = useState({
    user_id: '',
    lat: '',
    lon: '',
    image: '',
    keywords: [],
    description: '',
  });

  const handleInputChange = (e) => {
    setNewItem({
      ...newItem,
      [e.target.name]: e.target.value,
    });
  };

  const handleKeywordsChange = (e) => {
    // Split keywords into an array
    const keywordsArray = e.target.value.split(',');
    setNewItem({
      ...newItem,
      keywords: keywordsArray,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(newItem);
    setNewItem({
      user_id: '',
      lat: '',
      lon: '',
      image: '',
      keywords: [],
      description: '',
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="user_id"
        value={newItem.user_id}
        onChange={handleInputChange}
        placeholder="user_id"
      />
      <input
        type="text"
        name="lat"
        value={newItem.lat}
        onChange={handleInputChange}
        placeholder="lat"
      />
      <input
        type="text"
        name="lon"
        value={newItem.lon}
        onChange={handleInputChange}
        placeholder="lon"
      />
      <input
        type="text"
        name="image"
        value={newItem.image}
        onChange={handleInputChange}
        placeholder="image"
      />
      <input
        type="text"
        name="keywords"
        value={newItem.keywords.join(',')}
        onChange={handleKeywordsChange}
        placeholder="keywords"
      />
      <textarea
        name="description"
        value={newItem.description}
        onChange={handleInputChange}
        placeholder="description"
      ></textarea>
      <button type="submit">Create Item</button>
    </form>
  );
};

export default CreateItemForm;