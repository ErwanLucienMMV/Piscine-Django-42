def state():
    import sys

    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    if len(sys.argv) != 2:
        return
    for name, abbreviation in states.items():
        if capital_cities[abbreviation] == sys.argv[1]:
            print(name)
            return
    print("Unknown capital city")


if __name__ == '__main__':
    state()
