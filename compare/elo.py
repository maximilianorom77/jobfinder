#!/usr/bin/env python
import random
import json
import sys
import tty
import os

from collections import OrderedDict
from contextlib import contextmanager
from elote.arenas.lambda_arena import LambdaArena


fileno = sys.stdin.fileno()
try:
    cbreak = tty.tcgetattr(fileno)
except:
    cbreak = None

state_path = "competitors_state.json"


@contextmanager
def tmp_stdin_raw():
    tty.setraw(fileno)
    try:
        yield
    finally:
        tty.tcsetattr(fileno, 0, cbreak)

@contextmanager
def tmp_stdin_cbreak():
    old = tty.tcgetattr(fileno)
    tty.tcsetattr(fileno, 0, cbreak)
    try:
        yield
    finally:
        tty.tcsetattr(fileno, 0, old)

def print_words(word1, word2):
    line = 40
    l1 = len(word1)
    l2 = len(word2)
    margin = " " * 10
    spaces = " " * (line - (l1 + l2))
    print(f"{word1}{spaces}{word2}{margin}", end="")
    sys.stdout.flush()

def get_char(valids):
    while True:
        ch = sys.stdin.read(1)
        if ch in valids:
            break
    return ch

options = {
    "q": (True, 1),
    "w": (True, 2),
    "e": (True, 3),
    "r": (True, 4),
    "t": (True, 5),
    "a": (False, 1),
    "s": (False, 2),
    "d": (False, 3),
    "f": (False, 4),
    "g": (False, 5),
    "z": (None, 1)
}
valid_letters = list(options.keys())
def get_winner():
    ch = get_char(valid_letters)
    return options[ch]

def pick_and_pop(words):
    if words:
        i = random.randint(0, len(words) - 1)
        return words.pop(i)

def pick_two(words):
    word1 = pick_and_pop(words)
    word2 = pick_and_pop(words)
    return word1, word2

def ask(question):
    print(question, end="")
    sys.stdout.flush()
    ch = get_char(("y", "n"))
    print(ch, end="\r\n")
    return ch == "y"

@contextmanager
def swap_func(arena, func):
    old_func = None
    try:
        old_func = arena.func
        arena.func = func
        yield
    finally:
        if old_func:
            arena.func = old_func

def while_two(words, stop_at):
    while True:
        for n in range(stop_at):
            word1, word2 = pick_two(words)
            if not words:
                break
            yield word1, word2
        if not words:
            break
        if not ask("do you want to continue?: "):
            break

def export_initial_state(arena):
    return {k: {"initial_rating": v.rating} for k, v in arena.competitors.items()}

def save_initial_state():
    with open(state_path, "w") as state_file:
        state = export_initial_state(arena)
        state_file.write(json.dumps(state))

def get_state():
    return json.loads(open("competitors_state.json", "r").read())

def order_state(state):
    items = list(state.items())
    sort_items = lambda key: key[1]["initial_rating"]
    items.sort(key=sort_items, reverse=True)
    state = OrderedDict(items)
    return state

def get_top(state, n):
    state = order_state(state)
    return list(state.keys())[:30]

@contextmanager
def load_initial_state():
    kwargs = {}
    if os.path.exists(state_path):
        with open(state_path, "r") as state_file:
            state = json.loads(state_file.read())
            kwargs = {"initial_state": state}
    arena = LambdaArena(lambda a, b: None, **kwargs)
    try:
        yield arena
    finally:
        save_initial_state()

def print_board(arena):
    board = arena.leaderboard()
    print(json.dumps(board, indent=4), end="\r\n")

def read_counter():
    with open("words_counter.json", "r") as words_file:
        return json.loads(words_file.read())

def read_words():
    words_counter = read_counter()
    return list(words_counter.keys())


if __name__ == "__main__":
    words = read_words()
    with load_initial_state() as arena:
        # print_board(arena)
        with tmp_stdin_raw():
            for word1, word2 in while_two(words, 20):
                print_words(word1, word2)
                decision, n = get_winner()
                result = lambda a, b: decision
                with swap_func(arena, result):
                    for _ in range(n):
                        arena.matchup(word1, word2)
                if decision != None:
                    winner = word1 if decision else word2
                    print(f"{winner} x {n}", end="\n\r")
                else:
                    print("tie", end="\n\r")
                save_initial_state()
        # print_board(arena)
