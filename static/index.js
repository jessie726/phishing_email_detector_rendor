document.getElementById("emailForm").addEventListener("submit", async function(event) {
  event.preventDefault();

  const subject = document.getElementById("subject").value;
  const body = document.getElementById("body").value;
  const resultDiv = document.getElementById("result");

  resultDiv.innerHTML = "⏳ Checking...";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ subject, body })
    });

    const data = await response.json();
    resultDiv.innerHTML = `✅ Result: <span style="color: ${data.prediction === 'Phishing' ? 'red' : 'green'}">${data.prediction}</span>`;
  } catch (error) {
    console.error("Error:", error);
    resultDiv.innerHTML = "❌ Error connecting to backend.";
  }
});
