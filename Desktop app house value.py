import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
import os
from datetime import datetime

# --------------------------
# MODEL LOAD
# --------------------------
model = joblib.load("louisville_model.pkl")

# --------------------------
# FEATURES (ONLY YOUR 9)
# --------------------------
features = [
    "Crime Rate",
    "Industry Area",
    "Pollution Level",
    "Avg Rooms",
    "House Age",
    "Distance Employ",
    "Highway Access",
    "Tax Rate",
    "Education Ratio"
]

# --------------------------
# CSV FILE PATH (SAVE DATA HERE)
# --------------------------
csv_path = r"C:\Users\shars\myproject\louisville_housing.csv"

# --------------------------
# MAIN WINDOW
# --------------------------
app = tk.Tk()
app.title("House Value Prediction")
app.geometry("520x700")
app.configure(bg="#74ebd5")

entries = {}

# --------------------------
# TITLE
# --------------------------
title = tk.Label(
    app,
    text="🏠 House Value Prediction",
    font=("Arial", 18, "bold"),
    bg="#74ebd5"
)
title.pack(pady=10)

# --------------------------
# INPUT FIELDS
# --------------------------
for f in features:
    tk.Label(app, text=f, bg="#74ebd5", font=("Arial", 12)).pack()

    entry = tk.Entry(app, width=30)
    entry.pack(pady=5)

    entries[f] = entry

# --------------------------
# SAVE FUNCTION
# --------------------------
def save_to_csv(values, prediction):
    import pandas as pd
    import os
    from datetime import datetime

    file_path = r"C:\Users\shars\myproject\louisville_housing.csv"

    # ONLY KEEP FIRST 8 FEATURES (adjust if needed)
    values = values[:8]

    row = values + [prediction, datetime.now()]

    columns = [
        "crime_rate",
        "industry_area",
        "pollution_level",
        "avg_rooms",
        "house_age",
        "distance_employ",
        "highway_access",
        "tax_rate",
        "prediction",
        "timestamp"
    ]

    df_new = pd.DataFrame([row], columns=columns)

    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)

        # overwrite clean structure (prevents messy columns)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_csv(file_path, index=False)

    else:
        df_new.to_csv(file_path, index=False)
# --------------------------
# PREDICT FUNCTION
# --------------------------
def predict():
    try:
        values = []

        for f in features:
            val = float(entries[f].get())

            # validation (0–100 fields)
            if f in ["Crime Rate", "Industry Area", "Pollution Level", "Tax Rate", "Education Ratio"]:
                if val < 1 or val > 100:
                    messagebox.showerror("Error", "Values must be between 1 and 100")
                    return

            values.append(val)

        prediction = model.predict([values])[0]

        # SAVE RESULT
        save_to_csv(values, prediction)

        messagebox.showinfo(
            "Result",
            f"Predicted House Value: ${prediction:.2f}K"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --------------------------
# BUTTON
# --------------------------
btn = tk.Button(
    app,
    text="Predict",
    command=predict,
    bg="#4a90e2",
    fg="white",
    font=("Arial", 14),
    padx=10,
    pady=5
)
btn.pack(pady=20)

# --------------------------
# RUN APP
# --------------------------
app.mainloop()