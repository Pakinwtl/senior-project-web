import React, { useState } from "react";
import axios from "axios";

function UploadTest({ onResults }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [useModel, setUseModel] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("use_model", useModel);

    setLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/detect-trend",
        formData
      );
      console.log("API response:", response.data);
      onResults(response.data.results);
    } catch (err) {
      setError("An error occurred while uploading the file.");
      console.error(err);
      alert(err);
    } finally {
      setLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <h2>Upload Excel File</h2>
      <input
        type="file"
        accept=".xlsx"
        onChange={(e) => setFile(e.target.files[0])}
        required
      />
      <select onChange={(e) => setUseModel(e.target.value === "true")}>
        <option value="true">AI Model</option>
        <option value="false">Algorithm</option>
      </select>
      <button type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Detect Trend"}
      </button>
    </form>
  );
}

export default UploadTest;
