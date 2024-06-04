import React from "react";
import DeleteIcon from '@mui/icons-material/Delete';

function Card(props) {
  function handleClick() {
    props.onDelete(props.id);
  }

  return (
    <div className="card">
      <h1>Title: {props.title}</h1>
      <p>Content: {props.report}</p>
      <p>Municipality: {props.municipality}</p>
      <p>Year: {props.year}</p>
      <p>Population: {parseInt(props.population)}</p>
      <p>Percentage extrem poverty: {props.extreme_poverty_percentage}</p>
      <p>IDHM: {props.idhm}</p>
      <p>Author: {props.author}</p>
      <button onClick={handleClick}><DeleteIcon/></button>
    </div>
  );
}

export default Card;
