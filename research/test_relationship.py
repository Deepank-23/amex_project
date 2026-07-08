from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
	sys.path.insert(0, str(ROOT))

from src.preprocessing import preprocess_baseline
from src.customer_value import relationship_score

df = preprocess_baseline()

rel = relationship_score(df)

print(rel.describe())