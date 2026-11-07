def geohashing():
    import sys

    if len(sys.argv) != 4:
        raise ValueError(
            "Usage: python3 geohashing.py LATITUDE LONGITUDE YYYY-MM-DD-DOW"
        )
    latitude, longitude = float(sys.argv[1]), float(sys.argv[2])
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError("Latitude must be in [-90, 90], longitude in [-180, 180].")
    datedow = sys.argv[3]
    parts = datedow.split("-", 3)
    if len(parts) != 4 or list(map(len, parts[:3])) != [4, 2, 2]:
        raise ValueError("Use YYYY-MM-DD-DOW, for example 2005-05-26-10458.68.")
    year, month, day = map(int, parts[:3])
    days = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dow = float(parts[3])
    if not 1 <= year <= 9999 or not 1 <= month <= 12:
        raise ValueError("Invalid date.")
    if not 1 <= day <= days[month - 1] or not 0 < dow < float("inf"):
        raise ValueError("Invalid date or Dow Jones opening value.")
    import antigravity

    antigravity.geohash(latitude, longitude, datedow.encode("ascii"))


if __name__ == "__main__":
    try:
        geohashing()
    except (ValueError, UnicodeError) as error:
        print("Error:", error)
        raise SystemExit(1)
