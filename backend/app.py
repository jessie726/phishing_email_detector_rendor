from flask import Flask, request, jsonify
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences
from etl.load import load_pipeline
from etl.transform import clean_text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load once at startup
model, tokenizer, MAXLEN = load_pipeline(
    model_path="final_models/final_lstm.h5",
    tokenizer_path="final_models/tokenizer.pkl",
    drive_id="1G0VwRzWS2LmRfjSkkts8gbj902XJuA36",  # your Google Drive file ID
    maxlen=120
)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    subject = data.get("subject", "")
    body = data.get("body", "")

    text = subject + " " + body

    cleaned_text = clean_text(text)
    X = tokenizer.texts_to_sequences([cleaned_text])
    X = pad_sequences(X, maxlen=120, padding="post")
    y_pred = model.predict(X)[0][0] 

    result = "Phishing" if y_pred[0] > 0.5 else "Legitimate"
    return jsonify({"prediction": result, "score": float(y_pred)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
