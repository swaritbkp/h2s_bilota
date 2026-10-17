import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.engine import analyze


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            payload = {}
        else:
            payload = json.loads(raw_input)
    except Exception as exc:
        payload = {"_parse_error": str(exc)}

    result = analyze(payload)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
