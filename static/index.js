document.getElementById("emailForm").addEventListener("submit", async function(event) {
  event.preventDefault(); // stop default form reload

  const subject = document.getElementById("subject").value;
  const body = document.getElementById("body").value;
  const resultDiv = document.getElementById("result");
  const button = document.querySelector("button[type='submit']");

  // Reset button style before prediction
  button.style.backgroundColor = "#007bff"; // default blue
  button.textContent = "⏳ Checking...";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ subject, body })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Show result text
    resultDiv.innerHTML = `✅ Result: ${data.label} (${data.prediction})`;

    // Change button color based on label
    if (data.label === "Phishing") {
      button.style.backgroundColor = "red";
      button.textContent = "🚨 Phishing Detected!";
    } else {
      button.style.backgroundColor = "green";
      button.textContent = "✅ Legitimate Email";
    }
  } catch (error) {
    console.error("Error:", error);
    resultDiv.innerHTML = "❌ Error connecting to backend.";
    button.style.backgroundColor = "gray";
    button.textContent = "⚠️ Error";
  }
});
