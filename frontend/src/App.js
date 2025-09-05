import React, { useState } from "react";
import "./App.css";

function App() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!subject.trim() && !body.trim()) {
      alert("Please enter subject or body!");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("https://phishing-detector-backend-7z5b.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, body })
      });

      const data = await response.json();
      setResult(data.prediction);
    } catch (error) {
      console.error("Error:", error);
      setResult("Error connecting to backend");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>📧 Phishing Email Detector</h1>
      <input
        type="text"
        placeholder="Enter subject..."
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
      />
      <textarea
        rows="6"
        placeholder="Enter email body..."
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Checking..." : "Check Email"}
      </button>
      {result && <h2>Result: {result}</h2>}
    </div>
  );
}

export default App;