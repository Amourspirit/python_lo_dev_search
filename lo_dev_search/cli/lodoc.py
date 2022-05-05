#!/usr/bin/env python
# coding: utf-8
import sys
from ..web_search import search_lo_doc
def main() -> int:
    search = sys.argv[1:] 
    search_len = len(search)
    if search_len == 0:
        raise ValueError("Please provide an argument")
    arg1 = str(search.pop(0))
    arg2 = "" if search_len < 2 else search.pop(0)
    arg3 = "" if search_len < 3 else " ".join(search)
    search_lo_doc.search(arg1=arg1, arg2=arg2, arg3=arg3)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())