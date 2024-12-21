import pickle
import requests
from io import BytesIO

class HeightPredictor:
    def __init__(self):
        """
        Initializes the predictor by loading the scaler and model from GitHub URLs.
        """
        # Correct raw URLs for scaler and model
                          
        self.scaler_url ='https://raw.githubusercontent.com/PyBabaji/Babaji_Weight_height/main/Scalar.pkl'
        self.model_url = 'https://raw.githubusercontent.com/PyBabaji/Babaji_Weight_height/main/Regrassor.pkl'


        # Load the scaler from GitHub
        self.scaler = self.load_model_from_url(self.scaler_url)

        # Load the model from GitHub
        self.model = self.load_model_from_url(self.model_url)

    def load_model_from_url(self, url):
        """
        Loads a model from a given GitHub raw URL.
        """
        print(f"Loading model from {url}...")
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            model = pickle.load(BytesIO(response.content))  # Load the model directly from the response content
            return model
        else:
            raise Exception(f"Failed to download the model from {url}. Status code: {response.status_code}")

    def predict(self, weight):
        """
        Predicts the height for the given weight using the loaded model.
        """
        # Scale the input weight
        scaled_weight = self.scaler.transform([[weight]])[0][0]

        # Predict the height using the model
        predicted_height = self.model.predict([[scaled_weight]])[0]

        return predicted_height
