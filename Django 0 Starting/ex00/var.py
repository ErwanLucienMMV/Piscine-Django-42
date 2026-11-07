def my_var():
    integer = 42
    digits = "42"
    words = "quarante-deux"
    decimal = 42.0
    boolean = True
    sequence = [42]
    mapping = {42: 42}
    immutable = (42,)
    unique = set()

    for value in (integer, digits, words, decimal, boolean,
                  sequence, mapping, immutable, unique):
        print(value, "has a type", type(value))


if __name__ == '__main__':
    my_var()
