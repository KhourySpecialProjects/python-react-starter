"""Write the OpenAPI spec that FastAPI builds from the routes to backend/openapi.json."""

import json
import os
from pathlib import Path

# Importing the app reads settings, but building the spec never connects to the
# database, so a placeholder lets this run in CI.
os.environ.setdefault("DATABASE_URL", "postgresql://localhost/placeholder")

from app.main import app

output = Path(__file__).resolve().parents[1] / "openapi.json"
output.write_text(json.dumps(app.openapi(), indent=2) + "\n")
