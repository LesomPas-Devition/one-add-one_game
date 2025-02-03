# -*- coding: utf-8 -*-
from pprint import pp
import random

from utils import random_data, read_json
from errors import *

data_collection = read_json("../data/data_collection.json")

class Bot:
    def __init__(self, data=None, hands: tuple=(1, 1)):
        self.left = hands[0]
        self.right = hands[1]
        self.hands = [self.left, self.right]
        self.data = data if data is not None else random_data()

        self.step = 0

    def is_successful(self) -> bool:
        return True if self.hands == [0, 0] else False

    def probability(self, combination: tuple) -> float:
        return self.data[combination[0]-1][combination[1]-1]

    def choose(self, bot: 'Bot') -> int:
        operations = {}
        operation_code = 1
        for i in range(2):
            for j in range(2):
                if 0 in (self.hands[i], bot.hands[j]):
                    operation_code += 1
                    continue
                operations[operation_code] = (self.hands[i], bot.hands[j])
                operation_code += 1

        operation_to_probability = {self.probability(j): i for i, j in operations.items()}
        max_value = max(operation_to_probability.keys())

        if max_value < 0.05:
            return random.choice(list(operation_to_probability.values()))
        if self.step > 100 and self.step % 10:
            return random.choice(list(operation_to_probability.values()))
        return operation_to_probability[max_value]

    def operate(self, operation: int, bot: 'Bot') -> None:
        """
        operation:
        * 1 : left to left
        * 2 : left to right
        * 3 : right to left
        * 4 : right to right
        """
        self.step += 1

        match operation:
            case 1:
                if 0 in (self.left, bot.left):
                    raise OperationCodeError("You cannot select a hand with a value of 0")
                self.left = self._residual_add(self.left, bot.left)
                self.hands[0] = self.left
            case 2:
                if 0 in (self.left, bot.right):
                    raise OperationCodeError("You cannot select a hand with a value of 0")
                self.left = self._residual_add(self.left, bot.right)
                self.hands[0] = self.left
            case 3:
                if 0 in (self.right, bot.left):
                    raise OperationCodeError("You cannot select a hand with a value of 0")
                self.right = self._residual_add(self.right, bot.left)
                self.hands[1] = self.right
            case 4:
                if 0 in (self.right, bot.right):
                    raise OperationCodeError("You cannot select a hand with a value of 0")
                self.right= self._residual_add(self.right, bot.right)
                self.hands[1] = self.right

    def __dict__(self):
        return self.data

    def _residual_add(self, x: int, y: int, mold=10) -> int:
        return (x + y) % mold

class Game:
    def __init__(self, bot1: Bot, bot2: Bot):
        self.bot1 = bot1
        self.bot2 = bot2

    def run(self) -> Bot:
        if self.bot1.is_successful(): return self.bot1
        if self.bot2.is_successful(): return self.bot2

        if random.choice([True, False]):
            self.bot2.operate(operation=self.bot2.choose(self.bot1), bot=self.bot1)
            if self.bot2.is_successful(): return self.bot2

        while True:
            # bot1
            self.bot1.operate(operation=self.bot1.choose(self.bot2), bot=self.bot2)
            if self.bot1.is_successful(): return self.bot1

            # bot2
            self.bot2.operate(operation=self.bot2.choose(self.bot1), bot=self.bot1)
            if self.bot2.is_successful(): return self.bot2

            if self.bot1.step > 200:
                return random.choice((self.bot1, self.bot2))


def main() -> None:
    a = Bot(data=random.choice(data_collection))
    b = Bot(data=random.choice(data_collection))
    g = Game(a, b)
    bot = g.run()

    print("#" * 20)
    print("bot step:", bot.step)


if __name__ == '__main__':
    main()
