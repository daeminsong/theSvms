from dotenv import load_dotenv
from os import getenv
import os.path

envFileName = os.path.expanduser('~/.env')
load_dotenv(envFileName)

def FRED_API_KEY():
    return getenv('FRED_API_KEY')



