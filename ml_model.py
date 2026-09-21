"""
ml_model.py
------------
Loads the trained At-Risk classifier and exposes a simple function
the rest of the app can call: predict_risk(attendance_pct, marks_pct).
"""

import sys
import os
import pandas as pd
import joblib

if getattr(sys, 'frozen', False):
    # Running as a packaged PyInstaller app - bundled data files live
    # in sys._MEIPASS, not next to this module's __file__.
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "at_risk_model.joblib")
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_risk(attendance_pct, marks_pct):
    model = _get_model()
    features = pd.DataFrame(
        [[attendance_pct, marks_pct]],
        columns=["attendance_pct", "marks_pct"]
    )
    prediction = model.predict(features)
    return prediction[0]