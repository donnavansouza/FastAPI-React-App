import React from "react";

function Card(props) {
  function handleClick() {
    props.onDelete(props.id);
  }

  return (
    <div className="card">
      <h1>Title: {props.title}</h1>
      <p>Content: {props.relatorio}</p>
      <p>Municipality: {props.municipio}</p>
      <p>Year: {props.ano}</p>
      <p>Population: {parseInt(props.populacao)}</p>
      <p>Percentage extrem poverty: {props.porc_extrema_pobreza}</p>
      <p>IDHM: {props.idhm}</p>
      <p>Author: {props.autor}</p>
      <button onClick={handleClick}>DELETE</button>
    </div>
  );
}

export default Card;
