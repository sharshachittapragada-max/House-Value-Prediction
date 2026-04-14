import os
import sys
import joblib
from flask import Flask, render_template, request

# --------------------------
# FIX: Get correct base path for EXE + normal run
# --------------------------
def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_path()

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
MODEL_PATH = os.path.join(BASE_DIR, "louisville_model.pkl")

# --------------------------
# FEATURES (ONLY YOUR 9)
# --------------------------
feature_columns = [
    'crime_rate',
    'industry_area',
    'pollution_level',
    'avg_rooms',
    'house_age',
    'distance_employ',
    'highway_access',
    'tax_rate',
    'education_ratio'
]

# --------------------------
# LOAD MODEL
# --------------------------
model = joblib.load(MODEL_PATH)

# --------------------------
# FLASK APP
# --------------------------
app = Flask(__name__, template_folder=TEMPLATE_DIR)

# --------------------------
# HOME
# --------------------------
@app.route('/')
def home():
    return render_template(
        'index.html',
        columns=feature_columns,
        title="House Value Prediction",
        tip="Enter approximate values. Prediction is not exact."
    )

# --------------------------
# PREDICT
# --------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = []

        for col in feature_columns:
            value = float(request.form[col])

            if col in ['crime_rate', 'industry_area', 'pollution_level', 'tax_rate', 'education_ratio']:
                if value < 1 or value > 100:
                    return render_template(
                        'index.html',
                        columns=feature_columns,
                        title="House Value Prediction",
                        prediction_text="❌ Value must be between 1 and 100",
                        tip="Use approximate values."
                    )

            features.append(value)

        prediction = model.predict([features])[0]

        return render_template(
            'index.html',
            columns=feature_columns,
            title="House Value Prediction",
            prediction_text=f"Predicted House Value: ${prediction:.2f}K",
            tip="Prediction is approximate."
        )

    except Exception as e:
        return render_template(
            'index.html',
            columns=feature_columns,
            title="House Value Prediction",
            prediction_text=f"Error: {str(e)}",
            tip="Fix inputs."
        )

# --------------------------
# AUTO OPEN BROWSER (ROBUST)
# --------------------------
if __name__ == '__main__':
    import webbrowser
    import threading
    import socket
    import time

    def open_browser():
        while True:
            try:
                socket.create_connection(("127.0.0.1", 5000), timeout=1)
                break
            except:
                time.sleep(0.5)

        webbrowser.open("http://127.0.0.1:5000/")

    threading.Thread(target=open_browser, daemon=True).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )