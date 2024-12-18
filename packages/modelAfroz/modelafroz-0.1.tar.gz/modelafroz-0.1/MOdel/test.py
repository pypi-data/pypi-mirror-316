import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from MOdel import MLModel

# URLs for your model and scaler pickle files
model_url = 'https://github.com/AfrozSheikh/ML-/raw/main/ML/Regression/regressor.pkl'
scaler_url = 'https://github.com/AfrozSheikh/ML-/raw/main/ML/Regression/scalar.pkl'

# Initialize the model with the URLs
model = MLModel(model_url, scaler_url)

# Load the California Housing dataset
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
target = pd.Series(data.target, name="Target")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df, target, test_size=0.2, random_state=42)

# Transform the test data using the loaded scaler
X_test_scaled = model.scaler.transform(X_test)

# Make predictions using the loaded model
predictions = model.predict(X_test_scaled)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print("Mean Squared Error:", mse)
