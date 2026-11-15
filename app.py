
from pathlib import Path
import runpy

# Execute the actual Streamlit application on every rerun.
APP_FILE = Path(__file__).resolve().parent / "ui" / "app.py"

runpy.run_path(str(APP_FILE))
