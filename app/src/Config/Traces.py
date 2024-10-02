import os
from dotenv import load_dotenv
load_dotenv()

USE_TEMPO = True
TEMPO_IP = os.getenv("TEMPO_IP","10.0.10.110")
TEMPO_PORT = os.getenv("TEMPO_PORT","4317")
