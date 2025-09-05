import React, { useState } from "react";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!input.trim()) {
      alert("Please enter some text!");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("https://phishing-detector-backend-7z5b.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input })
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
      <textarea
        rows="6"
        placeholder="Paste email text here..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Checking..." : "Check Email"}
      </button>
      {result && <h2>Result: {result}</h2>}
    </div>
  );
}

export default App;