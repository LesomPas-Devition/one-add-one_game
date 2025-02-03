# -*- coding: utf-8 -*-
from json import load
import random

from sys import path
path.append("../bot")
from bot import Bot
from errors import *
from utils import read_json

data = random.choice(read_json("../data/data_collection.json")) # p if (p := read_json("../data/data.json")) != [] else None

order = 0
user_settings = {
    "showBotOperation": True,
}

class UserAndBot:
    text_to_order = {"random": 0, "bot": 1, "user": 2, "0": 0, "1": 1, "2": 2}
    text_to_operation = {"ll": 1, "lr": 2, "rl": 3, "rr": 4, "1": 1, "2": 2, "3": 3, "4": 4}

    code_to_text = {1: "ll", 2: "lr", 3: "rl", 4: "rr"}

    def __init__(self, bot_hands=(1, 1), user_hands=(1, 1)):
        self.bot = Bot(hands=bot_hands, data=data)
        self.user = Bot(hands=user_hands)

    def start(self) -> None:
        print(
            "welcome to the game!\n",
            "version 1.0 beta, Power by LesomPas\n\n",
            "输入 start 开始游戏\n",
            "输入 quit 退出游戏\n",
            "输入 exit 退出程序\n",
            "输入 order 调整先/后手\n",
            "输入 setting 调整设置\n"
        )
        while True:
            command = input("|>> ")
            match command:
                case "start":
                    self.run()
                case "exit":
                    exit(0)
                case "order":
                    print("输入以调整先手: bot | user | random ")
                    order_input = input("|input> ")
                    order_init = UserAndBot.text_to_order.get(order_input)
                    
                    if order_init is None:
                        print("|error> 请重试")
                        continue

                    global order
                    order = order_init
                case "setting":
                    print(
                        f"a. 显示bot操作: {user_settings['showBotOperation']}\n"
                    )
                    print("输入编号以调整")
                    answer = input("|input> ")
                    if answer == "a":
                        user_settings['showBotOperation'] = not user_settings['showBotOperation']
                case _:
                    print("|error> 请重试")

    def run(self) -> None:

        if self.bot.is_successful():
            print("|reply> bot赢了, game over")
            return
        if self.user.is_successful():
            print("|reply> 你赢了, game over")
            return

        if order == 1 or (order == 0 and random.choice([True, False])):
            print("|reply> bot为先手")
            bot_operation = self.bot.choose(self.user)
            if user_settings['showBotOperation']:
                print(f"|bot_operation> {UserAndBot.code_to_text[bot_operation]}")
            self.bot.operate(operation=bot_operation, bot=self.user)
            print(f"|information  bot> You: {self.user.left} {self.user.right} | Bot: {self.bot.left} {self.bot.right} ")
            if self.bot.is_successful():
                print("|reply> bot赢了, game over")
                return
        else:
            print(f"|information user> You: {self.user.left} {self.user.right} | Bot: {self.bot.left} {self.bot.right} ")
            print("|reply> 你为先手")

        while True:
            # user
            operation = input("|command> ")
            if operation == "quit":
                return
            try:
                self.user.operate(operation=UserAndBot.text_to_operation[operation], bot=self.bot)
            except OperationCodeError:
                print("|error> 不可使用这个操作码")
                continue
            except KeyError:
                print("|error> 操作码错误")
                continue
    
            print(f"|information user> You: {self.user.left} {self.user.right} | Bot: {self.bot.left} {self.bot.right} ")
            if self.user.is_successful():
                print("|reply> 你赢了, game over")
                return

            # bot
            bot_operation = self.bot.choose(self.user)
            if user_settings['showBotOperation']:
                print(f"|bot_operation> {UserAndBot.code_to_text[bot_operation]}")
            self.bot.operate(operation=bot_operation, bot=self.user)
            print(f"|information  bot> You: {self.user.left} {self.user.right} | Bot: {self.bot.left} {self.bot.right} ")
            if self.bot.is_successful():
                print("|reply> bot赢了, game over")
                return

            if self.bot.step > 2000:
                print("|error> 超出次数")
                return


if __name__ == '__main__':
    game = UserAndBot()
    game.start()
