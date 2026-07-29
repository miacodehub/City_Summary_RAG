import json
import requests
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def fetch_wikipedia(city):
    """
    Fetch introductory extract from Wikipedia.
    """

    params = {
        "action": "query",
        "prop": "extracts",
        "titles": city,
        "explaintext": True,
        "exintro": False,
        "format": "json",
        "redirects": 1
    }

    url = "https://en.wikipedia.org/w/api.php"

    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    pages = data["query"]["pages"]

    page = next(iter(pages.values()))

    return page.get("extract", "")


def split_into_sections(text):
    """
    Very simple parser.

    Wikipedia plaintext uses headings like

    History
    =======
    """

    documents = []

    current_title = "Overview"
    current_text = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line.startswith("="):

            if current_text:
                documents.append({
                    "section": current_title,
                    "content": " ".join(current_text)
                })

            current_title = line.replace("=", "").strip()
            current_text = []

        else:
            current_text.append(line)

    if current_text:
        documents.append({
            "section": current_title,
            "content": " ".join(current_text)
        })

    return documents


def build_city(city):

    print(f"Downloading {city}...")

    text = fetch_wikipedia(city)

    if not text:

        print(f"No article found for {city}")

        return

    documents = split_into_sections(text)

    output = {
        "city": city,
        "documents": documents
    }

    filename = city.lower().replace(" ", "_").replace(",", "")

    outfile = DATA_DIR / f"{filename}.json"

    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"Saved {outfile}")


if __name__ == "__main__":
    build_city("Kyoto")