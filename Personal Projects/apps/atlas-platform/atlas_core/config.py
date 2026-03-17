from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_ROOT = Path(os.getenv("ATLAS_DATA_ROOT", BASE_DIR / "synthetic_companies"))