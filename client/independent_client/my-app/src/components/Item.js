import React from 'react';

const Item = ({ item, onDelete }) => {
  return (
    <li>
      <span>{item.id}</span>
      <span>{item.user_id}</span>
      <span>{item.lat}</span>
      <span>{item.lon}</span>
      <span>{item.keywords}</span>
      <span>{item.image}</span>
      <span>{item.description}</span>
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </li>
  );
};

export default Item;