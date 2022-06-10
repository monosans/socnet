from pathlib import Path

from decouple import AutoConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = AutoConfig(search_path=BASE_DIR / "config")
