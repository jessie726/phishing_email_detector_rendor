import os
import pickle
import gdown
from tensorflow.keras.models import load_model


def load_pipeline(
    model_path="final_models/final_lstm.h5",
    tokenizer_path="final_models/tokenizer.pkl",
    drive_id=None,
    maxlen=120
):

    # Download model from Google Drive if not found
    if not os.path.exists(model_path) and drive_id:
        url = f"https://drive.google.com/uc?id={drive_id}"
        print(f"Model not found locally. Downloading from {url} ...")
        gdown.download(url, model_path, quiet=False)

    # Load model
    model = load_model(model_path, compile=False)

    # Load tokenizer
    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"Tokenizer file not found: {tokenizer_path}")
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)

    print(f"Loaded model from {model_path} and tokenizer from {tokenizer_path}")
    return model, tokenizer, maxlen
