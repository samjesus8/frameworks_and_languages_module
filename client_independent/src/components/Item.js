import React from 'react';

const Item = ({ item, onDelete }) => {
  return (
    <li>
      <span data-field="id">{item.id}</span>
      <span data-field="user_id">{item.user_id}</span>
      <span data-field="lat">{item.lat}</span>
      <span data-field="lon">{item.lon}</span>
      <span data-field="keywords">{item.keywords}</span>
      <span data-field="image">{item.image}</span>
      <span data-field="description">{item.description}</span>
      <button data-action="delete" onClick={() => onDelete(item.id)}>Delete</button>
    </li>
  );
};

export default Item;