from flask import Flask, request, jsonify
import os
from etl.load import load_pipeline
from etl.transform import clean_text
from flask_cors import CORS
CORS(app)

# Load once at startup
model, tokenizer, MAXLEN = load_pipeline(
    model_path="final_models/final_lstm.h5",
    tokenizer_path="final_models/tokenizer.pkl",
    drive_id="1G0VwRzWS2LmRfjSkkts8gbj902XJuA36",  # your Google Drive file ID
    maxlen=120
)

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("email", "")

    # Preprocess the input
    X = clean_text([text], tokenizer, maxlen)
    y_pred = model.predict(X)

    result = "Phishing" if y_pred[0] > 0.5 else "Legit"
    return jsonify({"prediction": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
