#!/usr/bin/env python
import json
from elo import get_state, get_top


if __name__ == "__main__":
    state = get_state()
    top = get_top(state, 5)
    for word in top:
        print(word)