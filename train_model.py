import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Sample data (replace with your actual stock data)
data = {'Days': [1, 2, 3, 4, 5],
        'Price': [100, 102, 105, 107, 110]}
df = pd.DataFrame(data)

# Features and labels
X = df[['Days']]
y = df['Price']

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the model
with open('stock_price_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model trained and saved as 'stock_price_model.pkl'")
