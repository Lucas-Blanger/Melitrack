import os
import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]

if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

os.environ.setdefault("ML_SERVICE_TOKEN", "test-ml-token")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("HIVE_SERVICE_URL", "http://hive-service:8000")
