import React from "react";
import { useState } from "react";

function Municipality_card(props) {
  return (
    <div className="Municipality_card">
      <p>Municipality Name: {props.data.municipality_name}</p>
      <p>Year: {props.data.year}</p>
      <p>Population: {props.data.population}</p>
      <p>IDHM: {props.data.idhm}</p>
      <p>Extreme Poverty Percentage: {props.data.extreme_poverty_percentage}</p>
    </div>
  );
}

export default Municipality_card;
