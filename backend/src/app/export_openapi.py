"""Write the OpenAPI contract to backend/openapi.json.

The frontend generates its API client from that file, so run
`mise run client:generate` after changing a route or schema. With `--check`,
fail instead of writing if the file is out of date (used by CI).
"""

import json
import sys
from pathlib import Path

from app.main import app

OUTPUT = Path(__file__).resolve().parents[2] / "openapi.json"


def main() -> None:
    contract = json.dumps(app.openapi(), indent=2) + "\n"

    if "--check" not in sys.argv:
        OUTPUT.write_text(contract)
        print(f"wrote {OUTPUT}")
        return

    if not OUTPUT.exists() or OUTPUT.read_text() != contract:
        sys.exit("backend/openapi.json is out of date. Run: mise run client:generate")
    print("backend/openapi.json is up to date")


if __name__ == "__main__":
    main()
