# config.py
import os

BASE_URL = "http://192.168.1.8:5173/"
BROWSER = "chromium"      # chromium | firefox | webkit
TIMEOUT = 60000           # ms

CSV_FILE = "data/testdata.csv"  # ✅ CSV with credentials
ARTIFACTS_DIR = "artifacts"
REPORTS_DIR = "reports"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "Uploads")
