#!/usr/bin/env python3
import json

from database import JobsDB
from collections import OrderedDict


jobs_db = JobsDB()

def get_words_count():
    words_counter = {}
    for record in jobs_db.get_posts_words():
        words = record[0]
        for word in words.split():
            if word not in words_counter:
                words_counter[word] = 0
            words_counter[word] += 1
    return words_counter

def sort_count(item):
    return item[1]

def main():
    file_name = "words_counter.json"
    words_counter = get_words_count()
    words_counter_list = sorted(words_counter.items(), key=sort_count)
    dumped = json.dumps(OrderedDict(words_counter_list), indent=4)
    with open(file_name, "w") as counter_file:
        counter_file.write(dumped)
    print(f"Report Created in {file_name}")

if __name__ == "__main__":
    main()
