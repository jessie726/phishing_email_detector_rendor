from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle, os
from etl.load import load_pipeline

model, tokenizer, MAXLEN = load_pipeline(
    model_path="final_models/final_lstm.h5",
    tokenizer_path="final_models/tokenizer.pkl",
    drive_id="1G0VwRzWS2LmRfjSkkts8gbj902XJuA36",  # your Google Drive file ID
    maxlen=120
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # put your frontend in templates/index.html

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    email_text = ""

    if request.method == "POST":
        email_text = request.form.get("email_text", "")

        # Transform input
        seq = tokenizer.texts_to_sequences([email_text])
        padded = pad_sequences(seq, maxlen=MAXLEN)

        # Predict
        pred = model.predict(padded)[0][0]
        prediction = f"Phishing ({pred:.2%})" if pred > 0.5 else f"Legitimate ({1-pred:.2%})"

    return render_template("index.html", prediction=prediction, email_text=email_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

