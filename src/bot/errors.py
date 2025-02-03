# -*- coding: utf-8 -*-


class OperationCodeError(RuntimeError):
    def __init__(self, msg):
        self.msgs = msg

    def __str__(self):
        return self.msgs