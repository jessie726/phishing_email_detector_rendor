from flask import Flask, request, render_template, jsonify
#from tensorflow.keras.models import load_model
import pickle, os
from etl.load import load_pipeline

model = load_pipeline(
    model_path="final_models/final_tfidf.pkl"
    #tokenizer_path="final_models/tokenizer.pkl",
    #drive_id="1G0VwRzWS2LmRfjSkkts8gbj902XJuA36",
)

app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def home():
#     return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    subject = data.get("subject", "")
    body = data.get("body", "")
    text = subject + " " + body
        
    pred = model.predict([text])[0]
    prob = model.predict_proba([text])[0][1]
    result = "Phishing" if pred == 1 else "Legitimate"
    prediction = prob if pred == 1 else 1 - prob

    return jsonify({
    "label": result,
    "prediction": f"{prediction:.2%}"
})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

