# -*- coding: utf-8 -*-
import functools


def calc_sum(*args):
    if args:
        return sum(args)
    return 0


def calc_diff(*args):
    if args:
        return functools.reduce(lambda a, b: a - b, args)
    return 0


def calc_mul(*args):
    if args:
        return functools.reduce(lambda a, b: a * b, args)
    return 1


def calc_div(*args):
    if args:
        return functools.reduce(lambda a, b: a / b, args)
    return 1


class Calculator:

    ops = {
        '+': calc_sum,
        '-': calc_diff,
        '*': calc_mul,
        '/': calc_div,
    }

    def __init__(self, output):
        self._chars = ''
        self._nums = []
        self.output = output

    def read(self, stream):
        while True:
            try:
                self.read_one(stream)
            except ZeroDivisionError:
                self.output.write('Cannot divide by zero\n')
            except (EOFError, KeyboardInterrupt):
                break

    def read_one(self, stream):
        character = stream.read(1)
        if character in self.ops:
            self.calclulate(character)
        elif character.isspace():
            self.push_number(character)
        elif character.isdigit():
            self.push_char(character)
        else:
            self.output.write('Not sure what you mean\n')

    def calclulate(self, op):
        if self._chars:
            self.push_number(op)
        nums = self._nums
        self._nums = []
        self.output.write('= {}\n'.format(self.ops[op](*nums)))

    def push_number(self, space):
        if self._chars:
            self._nums.append(int(self._chars))
            self._chars = ''

    def push_char(self, character):
        self._chars += character
