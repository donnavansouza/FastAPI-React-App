"use client";
import Image from "next/image";
import styles from "./page.module.css";
import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./Header";
import Footer from "./Footer";
import Card from "./Card";
import CreateArea from "./CreateArea";
import Municipality_card from "./Municipality_card";
import SearchMunYearCard from "./SearchMunYearCard";



export default function Home() {
  const [notes, setNotes] = useState([]);

  async function addNote(newNote) {
    try {
      const response = await axios.put(`http://localhost:500/relatorios/${id}`, {
        titulo: String(newNote.title),
        relatorio: String(newNote.content),
        autor: String(newNote.autor),
        municipio: Data_mun_card.municipality_name,
        ano: Data_mun_card.year
      });
      console.log("oi)");
      console.log(response.data);
      setData_mun_card({
        municipality_name: response.data.municipio,
        year: response.data.ano,
        population: response.data.populacao,
        extreme_poverty_percentage: response.data.porc_extrema_pobreza,
        idhm: response.data.IDHM,
      });
    }catch (error) {
      console.error('Error fetching municipality data:', error);
    }
  }

  function deleteNote(id) {
    setNotes(prevNotes => {
      return prevNotes.filter((noteItem, index) => {
        return index !== id;
      });
    });
  }

  const [Data_mun_card, setData_mun_card] = useState({
    municipality_name: "",
    year: "",
    population: "",
    extreme_poverty_percentage: "",
    idhm: "",
  });

  const [id, setId] = useState(0);

  async function renderMunicipalityData(municipality_name, year) {
    try {
      const response = await axios.post('http://localhost:500/relatorios', {
        titulo: "Some Title",
        relatorio: "Some Report Content",
        autor: "Author Name",
        municipio: municipality_name,
        ano: String(year)
      });
      setId(response.data.id);
      console.log(response.data);
      setData_mun_card({
        municipality_name: response.data.municipio,
        year: response.data.ano,
        population: response.data.populacao,
        extreme_poverty_percentage: response.data.porc_extrema_pobreza,
        idhm: response.data.idhm,
      });
    }catch (error) {
      console.error('Error fetching municipality data:', error);
    }
  }

  return (
    <div>
      <Header />
      <CreateArea onAdd={addNote} />
      <SearchMunYearCard function_render_mun_year={renderMunicipalityData} />
      <Municipality_card data={Data_mun_card} />
      {notes.map((noteItem, index) => {
        return (
          <Card
            key={index}
            id={index}
            title={noteItem.title}
            content={noteItem.content}
            onDelete={deleteNote}
          />
        );
      })}
      <Footer />
    </div>
  );
}
