# -*- coding: utf-8 -*-
import math
import random
from pprint import pp

from bot import Bot, Game
from utils import random_data, read_json, write_json

data_collection_file = "../data/data_collection.json"

population_num = 512
times = 1024

variant_probability = 0.1

class Training:
    def __init__(self, population_num: int, data=None):
        self.population = self._supplementary([Bot() for _ in range(population_num)] if data is None else [Bot(data=i) for i in data])
        self.population_num = population_num

    def vs(self):
        collection1, collection2 = to_half(self.population)
        self.successful_bots = []

        for bot1, bot2 in zip(collection1, collection2):
            self.successful_bots.append(Game(bot1, bot2).run())

    def heredity_and_variation(self) -> None:
        self.successful_bots.sort(key=fitness, reverse=True)
        heredity, variantion = to_half([i.data for i in self._supplementary(self.successful_bots)])

        self.population = self._heredity(heredity) + self._variantion(variantion)
        # pp(self.population)
        self.population = [Bot(data=data) for data in self.population][:self.population_num]

    def _heredity(self, sequence: list[list[list[float]]]) -> list[list[list[float]]]:
        first = sequence[0]
        sequence_length = len(sequence)
        father_collection = sequence.copy()
        mother_collection = sequence.copy()

        row = len(sequence[0][0])

        result = []
        for i in range(sequence_length):
            father = father_collection.pop(random.randint(0, sequence_length-1-i))
            mother = mother_collection.pop(random.randint(0, sequence_length-1-i))

            new_individual1 = []
            new_individual2 = []

            point1, point2 = random.randint(0, row-1), random.randint(0, row-1)
            # 确保切点顺序正确
            if point1 > point2:
                point1, point2 = point2, point1

            for line1, line2 in zip(father, mother):
                new_individual_pack1, new_individual_pack2 = self._point_twocrossover(line1, line2, point1, point2)

                new_individual1.append(new_individual_pack1); new_individual2.append(new_individual_pack2)
            result.append(new_individual1); result.append(new_individual2)

        return [first] + result[1:]


    def _point_twocrossover(self, chromosome1, chromosome2, point1: int, point2: int):
        new_chromosome1 = chromosome1[:point1] + chromosome2[point1:point2] + chromosome1[point2:]
        new_chromosome2 = chromosome2[:point1] + chromosome1[point1:point2] + chromosome2[point2:]

        return new_chromosome1, new_chromosome2


    def _variantion(self, sequence: list[list[list[float]]]) -> list[list[list[float]]]:
        variantion = []

        for data in sequence:
            column = random.randint(0, 8)
            for row in range(len(data)):
                if random.random() < variant_probability:
                    data[row][column] = random.random()

            variantion.append(data)
        return sequence + variantion


    def _supplementary(self, sequence: list) -> list:
        if len(sequence) % 2 == 1:
            sequence.append(Bot())
        return sequence


def to_half(sequence: list) -> list:
    half_length = len(sequence) // 2
    segment1 = sequence[:half_length]
    segment2 = sequence[half_length:]
    return [segment1, segment2]


def fitness(bot: Bot) -> float:
    return 12 - math.log(2, bot.step)

def main() -> None:
    training = Training(population_num, data=read_json(data_collection_file))
    for i in range(times):
        print(i)
        training.vs()
        training.heredity_and_variation()

    write_json(data_collection_file, content=[i.data for i in training.population])

if __name__ == '__main__':
    main()