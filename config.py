BOT_NAME = "Study Mentor Bot"

VERSION = "0.1"

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")