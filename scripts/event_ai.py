
import re
import unicodedata

GENRES = {
    "Hard Techno": ["hard techno", "industrial techno", "schranz"],
    "Drum & Bass": ["drum and bass", "drum & bass", "dnb", "jungle"],
    "Trance": ["trance", "psytrance", "goa"],
    "Techno": ["techno", "detroit techno", "minimal techno"],
    "House": ["house", "deep house", "tech house", "afro house"],
    "Electronic": ["electronic", "electro", "rave", "breakbeat", "garage"],
}

EXCLUDED = [
    "candlelight", "classical concert", "tribute concert",
    "symphony", "orchestra", "opera", "stand-up comedy",
]

def normalize(text):
    text = unicodedata.normalize("NFKC", str(text or ""))
    return text.casefold()

def classify_event(event):
    """Return a genre for a likely electronic event, or None."""
    name = normalize(event.get("name", ""))
    description = normalize(event.get("description", ""))
    genre = normalize(event.get("genre", ""))

    combined = " ".join([name, description, genre])

    if any(word in combined for word in EXCLUDED):
        return None

    for label, keywords in GENRES.items():
        if any(re.search(
            r"(?<!\w)" + re.escape(word) + r"(?!\w)",
            combined
        ) for word in keywords):
            return label

    return None


def is_athens_greece(event):
    """Reject known locations outside Athens, Greece."""
    country = normalize(event.get("country", ""))
    city = normalize(event.get("city", ""))

    if country and country not in ("gr", "greece", "ελλάδα", "ελλαδα"):
        return False

    if city and city not in ("athens", "αθήνα", "αθηνα", "athina"):
        return False

    return bool(country or city)


def filter_events(events):
    """Keep relevant events and remove duplicate URLs."""
    accepted = []
    seen = set()

    for event in events:
        if not is_athens_greece(event):
            continue

        genre = classify_event(event)
        if not genre:
            continue

        url = event.get("url", "")
        if not url or url in seen:
            continue

        seen.add(url)
        accepted.append({**event, "genre": genre})

    return accepted
