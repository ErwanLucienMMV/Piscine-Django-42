def display_numbers():
    with open("numbers.txt", encoding="utf-8") as source:
        for number in source.read().split(","):
            print(number.strip())


if __name__ == '__main__':
    display_numbers()
