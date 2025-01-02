import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

function App() {
  const [file, setFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Change endpoint depending on the type of file (image/video)
      const endpoint = file.type.startsWith("image")
        ? "http://localhost:8000/analyze/image/"
        : "http://localhost:8000/analyze/video/";

      const response = await axios.post(endpoint, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setAnalysisResult(response.data);  // Store the analysis result
    } catch (error) {
      console.error("Error analyzing file:", error);
      alert("An error occurred during the analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Media Analysis Tool</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Upload and Analyze"}
      </button>

      {analysisResult && (
        <div className="result">
          <h2>Analysis Results</h2>

          {/* Display metadata */}
          {analysisResult.metadata && (
            <div className="metadata">
              <h3>Metadata</h3>
              <pre>{JSON.stringify(analysisResult.metadata, null, 2)}</pre>
            </div>
          )}

          {/* Display ELA result */}
          {analysisResult.ela_result && (
            <div className="ela-analysis">
              <h3>Error Level Analysis (ELA)</h3>
              <pre>{JSON.stringify(analysisResult.ela_result, null, 2)}</pre>
            </div>
          )}

          {/* Display video anomalies */}
          {analysisResult.anomalies && (
            <div className="video-anomalies">
              <h3>Video Anomalies</h3>
              {analysisResult.anomalies.length > 0 ? (
                <ul>
                  {analysisResult.anomalies.map((anomaly, index) => (
                    <li key={index}>{anomaly}</li>
                  ))}
                </ul>
              ) : (
                <p>No anomalies detected.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
