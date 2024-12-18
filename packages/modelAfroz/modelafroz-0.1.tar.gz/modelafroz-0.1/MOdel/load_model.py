import pickle
import requests
from io import BytesIO

class MLModel:
    def __init__(self, model_url: str, scaler_url: str):
        """Initialize the MLModel with the URLs for the model and scaler."""
        self.model_url = model_url
        self.scaler_url = scaler_url
        self.model = self._load_model()
        self.scaler = self._load_scaler()

    def _load_model(self):
        """Download and load the model from the given GitHub URL."""
        response = requests.get(self.model_url)
        print(f"Model URL response status: {response.status_code}")  # Debugging line
        if response.status_code == 200:
            model_file = BytesIO(response.content)
            model = pickle.load(model_file)
            return model
        else:
            raise Exception(f"Failed to download model from GitHub. Status code: {response.status_code}")

    def _load_scaler(self):
        """Download and load the scaler from the given GitHub URL."""
        response = requests.get(self.scaler_url)
        print(f"Scaler URL response status: {response.status_code}")  # Debugging line
        if response.status_code == 200:
            scaler_file = BytesIO(response.content)
            scaler = pickle.load(scaler_file)
            return scaler
        else:
            raise Exception(f"Failed to download scaler from GitHub. Status code: {response.status_code}")

    def predict(self, data):
        """Make predictions using the loaded model."""
        if self.model is not None:
            return self.model.predict(data)
        else:
            raise Exception("Model not loaded successfully")
