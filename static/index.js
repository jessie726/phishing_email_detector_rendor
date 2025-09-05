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

    // Build result box
    if (data.label === "Phishing") {
      resultDiv.innerHTML = `
        <div style="background:#ffe6e6; padding:12px; border-radius:6px; color:#b30000; font-weight:bold;">
          ⚠️ Result: This email is classified as <span style="color:red">${data.label}</span> (${data.prediction})
        </div>`;
    } else {
      resultDiv.innerHTML = `
        <div style="background:#e6ffe6; padding:12px; border-radius:6px; color:#006600; font-weight:bold;">
          ✅ Result: This email is classified as <span style="color:green">${data.label}</span> (${data.prediction})
        </div>`;
    }
  } catch (error) {
    console.error("Error:", error);
    resultDiv.innerHTML = "❌ Error connecting to backend.";
  }
});
