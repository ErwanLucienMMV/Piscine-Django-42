def article_url(href):
    import requests

    if not isinstance(href, str):
        return None
    for prefix in ("https://en.wikipedia.org", "//en.wikipedia.org"):
        if href.startswith(prefix + "/"):
            href = href[len(prefix):]
            break
    if not href.startswith("/wiki/"):
        return None
    title = requests.utils.unquote(href[6:].split("#", 1)[0].split("?", 1)[0])
    if not title or ":" in title:
        return None
    return "https://en.wikipedia.org/wiki/" + requests.utils.quote(
        title.replace(" ", "_"), safe="()/,'!"
    )


def next_article(soup):
    redirect = soup.select_one(".redirectMsg a[href]")
    if redirect:
        return article_url(redirect.get("href"))
    content = soup.select_one("#mw-content-text .mw-parser-output")
    if content is None:
        content = soup.select_one(".mw-parser-output")
    if content is None:
        raise ValueError("Wikipedia article content was not found.")
    introduction = content.find("section", attrs={"data-mw-section-id": "0"},
                                recursive=False)
    if introduction is not None:
        content = introduction
    for child in content.children:
        if not getattr(child, "name", None):
            continue
        if child.name in ("h2", "h3") or child.select_one("h2"):
            break
        if child.name != "p":
            continue
        for link in child.find_all("a", href=True):
            destination = article_url(link["href"])
            if destination and not link.find_parent(["sup", "table"]):
                return destination
    return None


def roads_to_philosophy():
    import sys
    import requests
    from bs4 import BeautifulSoup

    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise ValueError('Usage: python3 roads_to_philosophy.py "article title"')
    query = sys.argv[1].strip()
    url = "https://en.wikipedia.org/w/index.php"
    parameters = {"search": query, "title": "Special:Search", "go": "Go"}
    visited = set()
    while True:
        response = requests.get(
            url, params=parameters,
            headers={"User-Agent": "PiscineDjangoLibraries/1.0 (educational CLI)"},
            timeout=20,
        )
        response.raise_for_status()
        parameters = None
        soup = BeautifulSoup(response.text, "html.parser")
        heading = soup.select_one("h1#firstHeading") or soup.find("h1")
        if heading is None or soup.select_one(".mw-search-results"):
            raise ValueError("No matching Wikipedia article found.")
        title = heading.get_text(" ", strip=True)
        if not title or title in ("Search results", "Special:Search"):
            raise ValueError("No matching Wikipedia article found.")
        key = title.replace("_", " ").casefold()
        if key in visited:
            print("It leads to an infinite loop !")
            return
        visited.add(key)
        print(title)
        if key == "philosophy":
            print(f"{len(visited)} roads from {query} to philosophy !")
            return
        url = next_article(soup)
        if url is None:
            print("It leads to a dead end !")
            return


if __name__ == "__main__":
    try:
        roads_to_philosophy()
    except Exception as error:
        print("Error:", error)
        raise SystemExit(1)
