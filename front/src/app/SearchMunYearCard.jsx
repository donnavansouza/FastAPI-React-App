import React, { useState } from "react";

function SearchMunYearCard(props) {
  const [formData, setFormData] = useState({
    Municipality_name: "",
    Year: "",
  });

  const handleInputChange = (event) => {
    const value =
      event.target.type === "checkbox"
        ? event.target.checked
        : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // You can handle the form submission here (e.g., send data to a server or perform a search)
    props.function_render_mun_year(formData.Municipality_name, formData.Year);

    // Reset the form after submission
    setFormData({
      Municipality_name: "",
      Year: "",
    });
  };

  return (
    <div className="SearchMunYearCard">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="Municipality_name"
          onChange={handleInputChange}
          placeholder="Municipality Name"
          value={formData.Municipality_name}
        />
        <input
          type="text"
          name="Year"
          onChange={handleInputChange}
          placeholder="Year"
          value={formData.Year}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default SearchMunYearCard;
