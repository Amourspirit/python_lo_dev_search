# coding: utf-8
import webbrowser
import sys
import argparse
from typing import List, Union
from ..api_search import search_api
from ..data_class.component import Component

# region Terminal Questions


def query_choice(comps: List[Component]) -> Union[int, None]:
    """
    Ask for a choice of wich component to open url for.

    Arguments:
        comps (List[Component]): List of components to choose from.

    Returns:
        (Union[int, None]): Integer representing the zero base index within comps or None if canceled.
    """
    # https://tinyurl.com/yyg38fp2
    # https://tinyurl.com/y2pv2cdh
    c_len = len(comps)
    # valid is 1 to length of comps + 1 for None
    valid = tuple([i for i in range(1, c_len + 1)])
    question = 'Choose an option (default 1):'
    prompt = f'\n{"[0],":<5} Cancel'
    for i, comp in enumerate(comps, 1):
        prompt = prompt + \
            f"\n{f'[{i}],':<5} {comp.name:<33} - {comp.id_component}"
        i += 1
    prompt += '\n'
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '':
            return 0
        if choice == 'q':
            return None
        if choice.isdigit():
            j = int(choice)
        else:
            j = -1
        if j == 0:
            return None
        if j in valid:
            return j - 1
        else:
            sys.stdout.write(f"Please respond with input from 0 - {c_len}\n")
# endregion Terminal Questions


def _args_comp(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-s', '--search',
        help=f"",
        action='store',
        dest='search',
        required=True
    )
    parser.add_argument(
        '-l', '--no-leading',
        help="No leading wildcard in search",
        action='store_false',
        dest='leading',
        default=True
    )
    parser.add_argument(
        '-t', '--no-trailing',
        help="No trailing wildcard in search",
        action='store_false',
        dest='trailing',
        default=True
    )
    parser.add_argument(
        '-m', '--max-results',
        help="Limits the number of results returned: Default 10",
        action='store',
        dest='limit',
        type=int,
        default=10
    )


def _args_comp_action(args: argparse.Namespace) -> int:
    search = "%".join(str(args.search).split())
    # print(search)
    if len(search) <= 2:
        print("Search requires at least 3 characters")
        return 0
    if args.leading:
        search = "%" + search
    if args.trailing:
        search = search + '%'
    results = search_api.search_component(search, limit=int(args.limit))
    if len(results) == 0:
        print('Search produced no results')
        return 0
    choice = query_choice(results)
    if choice is not None:
        url = results[choice].url
        webbrowser.open(url)
    return 0


def _args_process_cmd(args: argparse.Namespace) -> int:
    if args.command == "comp":
        return _args_comp_action(args)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='main')
    subparser = parser.add_subparsers(dest="command")
    cmd_comp = subparser.add_parser(
        name="comp", help="Search for components")
    _args_comp(cmd_comp)
    if len(sys.argv) <= 1:
        parser.print_help()
        return 0
    args = parser.parse_args()
    print(args)
    _args_process_cmd(args)

    return 0
