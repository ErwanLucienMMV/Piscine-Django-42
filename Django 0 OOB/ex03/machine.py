#!/usr/bin/env python3

import random
from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino


class CoffeeMachine:
    def __init__(self):
        self.served = 0

    class EmptyCup(HotBeverage):
        name = 'empty cup'
        price = 0.90

        def description(self):
            return 'An empty cup?! Gimme my money back!'

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__('This coffee machine has to be repaired.')

    def repair(self):
        self.served = 0

    def serve(self, beverage):
        if self.served >= 10:
            raise self.BrokenMachineException()
        if not isinstance(beverage, type) or not issubclass(beverage, HotBeverage):
            raise TypeError('Expected a HotBeverage subclass.')
        result = beverage() if random.randint(0, 1) else self.EmptyCup()
        self.served += 1
        return result


def main():
    machine = CoffeeMachine()
    beverages = (Coffee, Tea, Chocolate, Cappuccino)
    for cycle in range(2):
        try:
            for index in range(11):
                print(machine.serve(beverages[index % len(beverages)]))
        except CoffeeMachine.BrokenMachineException as error:
            print(error)
        if cycle == 0:
            machine.repair()


if __name__ == '__main__':
    main()
