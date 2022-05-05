#!/usr/bin/env python
# coding: utf-8
import webbrowser
import sys
import argparse
from typing import List, Union
from ..api_search import search_api
from ..data_class.component import Component

def query_choice(comps: List[Component]) -> Union[int, None]:
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    # https://tinyurl.com/yyg38fp2
    # https://tinyurl.com/y2pv2cdh
    c_len = len(comps)
    # valid is 1 to length of comps + 1 for None
    valid = tuple([i for i in range(1, c_len + 1)])
    question = 'Choose an option (default 1):'
    prompt = '\n[0], Cancel'
    i = 1
    for comp in comps:
        # if i == 1:
        #     prompt = prompt + f"\n[{i}] (default)), {comp.name}, {comp.id_component}"
        # else:
        prompt = prompt + f"\n[{i}], {comp.name}, {comp.id_component}"
        i += 1
    # prompt += f"\n[{i}] Cancel\n"
    prompt += '\n'
    # last = i
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '':
            return 0
        if choice.isdigit():
            j = int(choice)
        else:
            j = -1
        if j == 0:
            return None
        if j in valid:
            return j - 1
        else:
            choices = ','.join([str(i) for i in range(c_len + 1)])
            sys.stdout.write(f"Please respond with one of the following: {choices}\n")

def main() -> int:
    results = search_api.search_component("%time%", limit=15)
    choice = query_choice(results)
    if choice is not None:
        url = results[choice].url
        webbrowser.open(url)
    # for result in results:
    #     print(f"{result.name}, {result.id_component}")
    
    return 0