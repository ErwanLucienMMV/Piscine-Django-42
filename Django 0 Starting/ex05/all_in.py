def all_in():
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
    if len(sys.argv) != 2 or ",," in sys.argv[1]:
        return
    for expression in sys.argv[1].split(","):
        expression = " ".join(expression.split())
        if not expression:
            continue
        for state, abbreviation in states.items():
            capital = capital_cities[abbreviation]
            if expression.lower() in (state.lower(), capital.lower()):
                print(capital, "is the capital of", state)
                break
        else:
            print(expression, "is neither a capital city nor a state")


if __name__ == '__main__':
    all_in()
