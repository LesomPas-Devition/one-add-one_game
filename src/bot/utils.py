# -*- coding: utf-8 -*-
import random
import json

def random_data() -> list[list[int]]:
    data = []
    for _ in range(9):
        data_line = []
        for _ in range(9):
            data_line.append(random.uniform(0.01, 1.00))

        data.append(data_line)

    return data


# 读取json文件
def read_json(path: str, encoding: str="utf-8"):
    js = open(path, "r", encoding="utf-8")
    result = json.load(js)
    js.close()
    return result


# 写入json文件
def write_json(path: str, content, encoding: str="utf-8", indent=4) -> None:
    js = open(path, "w", encoding=encoding)
    json.dump(content, js, ensure_ascii=False, indent=indent)
    js.close()


if __name__ == '__main__':
    from pprint import pp
    pp(random_data())