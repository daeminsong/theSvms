import sys
from pathlib import Path 
root = Path(__file__).resolve().parents[1]
sys.path.append(str(root))

from keyCollection import FRED_API_KEY

print(FRED_API_KEY())