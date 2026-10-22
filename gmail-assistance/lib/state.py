"""Remember message IDs between runs without changing inbox read/unread status."""

import json


def save_processed(path, ids):
    pending = path.with_suffix(".pending")
    pending.write_text(json.dumps(sorted(ids), indent=2), encoding="utf-8")
    pending.replace(path)


def load_processed(path):
    return set(json.loads(path.read_text(encoding="utf-8")))
