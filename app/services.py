from re import sub
from uuid import uuid4


def make_slug(text):
    value = sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text.strip()).strip("-")
    return value[:120] or uuid4().hex[:12]


def normalize_text(value):
    return (value or "").strip()


def parse_int_list(values):
    ids = []
    for value in values:
        try:
            ids.append(int(value))
        except (TypeError, ValueError):
            continue
    return ids
