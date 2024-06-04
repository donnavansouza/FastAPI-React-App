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
  const [reports, setReports] = useState([]);


  async function addReport(newReport) {
    try {
      const response = await axios.put(`http://localhost:500/reports/${id}`, {
        title: String(newReport.title),
        report: String(newReport.content),
        author: String(newReport.author),
        municipality: Data_mun_card.municipality_name,
        year: Data_mun_card.year
      });
      console.log("oi)");
      console.log(response.data);
      setData_mun_card({
        municipality_name: response.data.municipality,
        year: response.data.year,
        population: response.data.population,
        extreme_poverty_percentage: response.data.extreme_poverty_percentage,
        idhm: response.data.IDHM,
      });
    } catch (error) {
      console.error('Error fetching municipality data:', error);
    }
  }

  async function deleteReport(id) {
    const response = await axios.delete(`http://localhost:500/reports/${id}`);
    console.log(response);
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
      const response = await axios.post('http://localhost:500/reports', {
        title: "Some Title",
        report: "Some Report Content",
        author: "Author Name",
        municipality: municipality_name,
        year: String(year)
      });
      setId(response.data.id);
      console.log(response.data);
      setData_mun_card({
        municipality_name: response.data.municipality,
        year: response.data.year,
        population: response.data.population,
        extreme_poverty_percentage: response.data.extreme_poverty_percentage,
        idhm: response.data.idhm,
      });
    } catch (error) {
      console.error('Error fetching municipality data:', error);
    }
  }

  try {
    useEffect(() => {
      async function fetchData() {
        try {
          const response = await axios.get('http://localhost:500/reports');
          console.log(response.data);
          setReports(response.data);

        } catch (error) {
          console.error('Error fetching reports:', error);
        }
      }
      fetchData();
    }, []);
  } catch (error) {
    console.error('Error fetching reports:', error);
  }

  return (
    <div className="container">
      <div className="header">
        <Header />
      </div>
      <div className="content-container">
        <div className="create-area">
          <CreateArea onAdd={addReport} />
        </div>
        <div className="right-content">
          <div className="search-mun-year-card">
            <SearchMunYearCard function_render_mun_year={renderMunicipalityData} />
          </div>
          <div className="municipality-card">
            <Municipality_card data={Data_mun_card} />
          </div>
        </div>
      </div>
      <div className="reports">
        {reports.map((reportItem, index) => {
          return (
            <div className="report-card" key={index}>
              <Card
                id={reportItem.id}
                author={reportItem.author}
                title={reportItem.title}
                report={reportItem.report}
                municipality={reportItem.municipality}
                year={reportItem.year}
                population={reportItem.population}
                extreme_poverty_percentage={reportItem.extreme_poverty_percentage}
                idhm={reportItem.idhm}
                onDelete={deleteReport}
              />
            </div>
          );
        })}
      </div>
      <div className="footer">
        <Footer />
      </div>
    </div>
  );

}
