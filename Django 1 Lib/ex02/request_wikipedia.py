def api_request(parameters):
    import requests

    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={"format": "json", "formatversion": 2, "utf8": 1, **parameters},
        headers={"User-Agent": "PiscineDjangoLibraries/1.0 (educational CLI)"},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise ValueError(data["error"].get("info", "Wikipedia API error."))
    return data


def search_page(query):
    for attempt in range(2):
        data = api_request({"action": "query", "list": "search",
                            "srsearch": query, "srlimit": 1,
                            "srinfo": "suggestion", "srprop": ""})
        results = data.get("query", {}).get("search", [])
        if results:
            return results[0]["pageid"]
        suggestion = data.get("query", {}).get("searchinfo", {}).get("suggestion")
        if attempt or not suggestion:
            break
        query = suggestion
    raise ValueError("No Wikipedia article found for this search.")


def request_wikipedia():
    import sys
    import dewiki

    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise ValueError('Usage: python3 request_wikipedia.py "search terms"')
    query = sys.argv[1].strip()
    pageid = search_page(query)
    data = api_request({"action": "query", "prop": "revisions",
                        "pageids": pageid, "rvprop": "content", "rvslots": "main",
                        "redirects": 1})
    pages = data.get("query", {}).get("pages", [])
    if not pages or "missing" in pages[0] or not pages[0].get("revisions"):
        raise ValueError("The selected Wikipedia article is unavailable.")
    markup = pages[0]["revisions"][0]["slots"]["main"]["content"]
    text = dewiki.from_string(markup).strip()
    if not text:
        raise ValueError("The selected article contains no readable text.")
    filename = "".join("_" if character.isspace() or character in '/\\:*?"<>|'
                       or ord(character) < 32 else character for character in query)
    filename = filename.strip(". ")
    if not filename:
        raise ValueError("The search cannot be used as a filename.")
    with open(filename + ".wiki", "w", encoding="utf-8") as output:
        output.write(text + "\n")


if __name__ == "__main__":
    try:
        request_wikipedia()
    except Exception as error:
        print("Error:", error)
        raise SystemExit(1)
