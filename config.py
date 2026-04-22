import os
from dotenv import load_dotenv

load_dotenv()

# reqres.in API key (get a free key at https://reqres.in)
REQRES_API_KEY = os.getenv("REQRES_API_KEY", "")
