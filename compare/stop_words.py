#!/usr/bin/env python3
import sys
import tty
import json
import time
from collections import OrderedDict


class Buckets:

    def __init__(self, buckets_number):
        self.files = {}
        self.words = {}
        self.open_buckets(buckets_number)

    def open_buckets(self, num):
        for n in range(1, num + 1):
            bucket = open(f"bucket_{n}.txt", "a+")
            bucket.seek(0)
            self.files[n] = bucket
            self.words[n] = set(bucket.read().split())

    def write_to(self, n, word):
        self.words[n].add(word)
        bucket = self.files[n]
        bucket.write(f"{word}\n")
        bucket.flush()

    def has(self, word):
        for words in self.words.values():
            if word in words:
                return True
        return False


def main():
    buckets_number = 3
    buckets_nums = list(range(1, buckets_number + 1))
    buckets = Buckets(buckets_number)
    counter = json.loads(open("words_counter.json", "r").read())
    tty.setraw(sys.stdin.fileno())
    for word in counter.keys():
        if buckets.has(word):
            continue
        print(word, end=': ')
        sys.stdout.flush()
        while True:
            try:
                ch = int(sys.stdin.read(1))
            except ValueError:
                continue
            if ch in buckets_nums:
                break
        buckets.write_to(ch, word)
        print(ch, end="\n\r")


if __name__ == "__main__":
    main()


