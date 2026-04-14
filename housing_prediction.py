import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Check if the model file exists; if not, train and save the model.
MODEL_FILENAME = 'model.pkl'
if not os.path.exists(MODEL_FILENAME):
    # Load the Boston Housing dataset from a URL
    url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
    df = pd.read_csv(url)
    X = df.drop(columns=['medv'])  # Features
    y = df['medv']                # Target variable (house price)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Save the trained model to a file
    joblib.dump(model, MODEL_FILENAME)
else:
    # Load the saved model
    model = joblib.load(MODEL_FILENAME)

# Create the Tkinter window
root = tk.Tk()
root.title("Boston House Price Prediction")
root.geometry("350x600")

# Define the feature names (from the Boston Housing dataset)
features = [
    "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", 
    "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
]

# Dictionary to store entry widgets for each feature
entries = {}

# Create a label and entry widget for each feature
for feature in features:
    frame = tk.Frame(root)
    frame.pack(pady=5, padx=10, anchor='w')
    label = tk.Label(frame, text=f"{feature}: ", width=15, anchor='w')
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame, width=20)
    entry.pack(side=tk.RIGHT)
    entries[feature] = entry

# Define the prediction function
def predict():
    try:
        # Retrieve values from the entries and convert them to floats
        values = [float(entries[feature].get()) for feature in features]
        # Predict using the trained model
        prediction = model.predict([values])[0]
        # Display the prediction in a message box
        messagebox.showinfo("Prediction", f"Predicted House Price: ${prediction:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create a button to trigger prediction
predict_button = tk.Button(root, text="Predict", command=predict, bg="blue", fg="white", padx=10, pady=5)
predict_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
