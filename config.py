# config.py
import os

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "path/to/chromedriver")  # Update path or set via environment variable
OUTPUT_PATH = os.getenv("OUTPUT_PATH", os.path.expanduser("~/Desktop"))       # Default to Desktop
BASE_URL = "https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisSonuclari?SehirId=82&SehirAdi=Keeneland+ABD"
DAYS_BACK = 100                                                               # Number of days to go back in history
