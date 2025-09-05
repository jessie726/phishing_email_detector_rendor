from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle, os

app = Flask(__name__)

model = load_model("final_models/final_lstm.h5")
with open("final_models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
maxlen = 100

@app.route("/")
def home():
    return render_template("index.html")  # put your frontend in templates/index.html

@app.route("/predict", methods=["POST"])
def predict():
    subject = request.form.get("subject", "")
    body = request.form.get("body", "")
    text = subject + " " + body
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=maxlen, padding="post")
    y_pred = model.predict(padded)
    result = "Phishing" if y_pred[0][0] > 0.5 else "Legitimate"
    return jsonify({"prediction": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

