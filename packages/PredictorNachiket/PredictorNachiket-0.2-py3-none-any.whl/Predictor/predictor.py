import pickle
import requests
import numpy as np
import io

# URL to your .pkl file on GitHub
MODEL_URL = "https://raw.githubusercontent.com/Nachiket858/ML_Regression/main/Simple/model.pkl"

class Predictor:
    def __init__(self):
        """Initialize the predictor by loading the model."""
        self.model = self._load_model()

    def _load_model(self):
        """Fetch and load the model from the GitHub URL."""
        try:
            response = requests.get(MODEL_URL)
            response.raise_for_status()  # Check for HTTP request errors
            return pickle.load(io.BytesIO(response.content))
        except Exception as e:
            raise RuntimeError(f"Error loading model: {e}")

    def predict(self, features):
        """
        Predict based on input features.
        :param features: List of features (2D array or list of lists)
        :return: Predictions as a list
        """
        features = np.array(features)
        return self.model.predict(features).tolist()
