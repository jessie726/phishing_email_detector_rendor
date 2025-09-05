from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
import pickle, os
from etl.load import load_pipeline

model, tokenizer, MAXLEN = load_pipeline(
    model_path="final_models/final_tfidf.pkl",
    tokenizer_path="final_models/tokenizer.pkl",
    drive_id="1G0VwRzWS2LmRfjSkkts8gbj902XJuA36",  # your Google Drive file ID
    maxlen=120
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    email_text = ""

    if request.method == "POST":
        email_text = request.form.get("email_text", "")

        # Transform input using TF-IDF
        X = tokenizer.transform([email_text])

        # Predict
        pred = model.predict_proba(X)[0]
        phishing_prob = pred[1]
        legit_prob = pred[0]

        prediction = f"Phishing ({phishing_prob:.2%})" if phishing_prob > 0.5 else f"Legitimate ({legit_prob:.2%})"

    return render_template("index.html", prediction=prediction, email_text=email_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

