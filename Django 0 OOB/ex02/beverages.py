#!/usr/bin/env python3


class HotBeverage:
    price = 0.30
    name = 'hot beverage'

    def description(self):
        return 'Just some hot water in a cup.'

    def __str__(self):
        return 'name : {}\nprice : {:.2f}\ndescription : {}'.format(
            self.name, self.price, self.description())


class Coffee(HotBeverage):
    name = 'coffee'
    price = 0.40

    def description(self):
        return 'A coffee, to stay awake.'


class Tea(HotBeverage):
    name = 'tea'


class Chocolate(HotBeverage):
    name = 'chocolate'
    price = 0.50

    def description(self):
        return 'Chocolate, sweet chocolate...'


class Cappuccino(HotBeverage):
    name = 'cappuccino'
    price = 0.45

    def description(self):
        return "Un po' di Italia nella sua tazza!"


def main():
    for beverage in (HotBeverage, Coffee, Tea, Chocolate, Cappuccino):
        print(beverage())


if __name__ == '__main__':
    main()
