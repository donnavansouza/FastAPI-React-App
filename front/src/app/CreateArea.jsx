import React, { useState } from "react";

function CreateArea(props) {
  const [report, setReport] = useState({
    title: "",
    content: "",
    author: ""
  });

  function handleChange(event) {
    const { name, value } = event.target;

    setReport(prevReport => {
      return {
        ...prevReport,
        [name]: value
      };
    });
  }

  function submitReport(event) {
    props.onAdd(report);
    setReport({
      title: "",
      content: "",
      author: ""
    });
    event.preventDefault();
  }

  return (
    <div className="createArea">
      <form>
        <input
          name="title"
          onChange={handleChange}
          value={report.title}
          placeholder="Title"
        />
        <textarea
          name="content"
          onChange={handleChange}
          value={report.content}
          placeholder="Write a report..."
          rows="8"
        />
        <input
          name="author"
          onChange={handleChange}
          value={report.author}
          placeholder="Author"
        />
        <button onClick={submitReport}>Add</button>
      </form>
    </div>
  );
}

export default CreateArea;
