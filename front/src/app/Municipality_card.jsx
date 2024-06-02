import React from "react";
import { useState } from "react";

function Municipality_card(props) {
  return (
    <div className="Municipality_card">
      <p>Nome do Município: {props.data.municipality_name}</p>
      <p>Ano: {props.data.year}</p>
      <p>População: {props.data.population}</p>
      <p>IDHM: {props.data.idhm}</p>
      <p>Porcentagem Extrema Pobreza: {props.data.extreme_poverty_percentage}</p>
    </div>
  );
}

export default Municipality_card;
