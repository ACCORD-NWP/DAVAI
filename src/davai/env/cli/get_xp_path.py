#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Get path of a Davai experiment
"""
import argparse

from ..experiment import XP

__all__ = ['main']


def main():
    parser = argparse.ArgumentParser(description="Get path of a Davai experiment")
    parser.add_argument('experiment',
                        help=" ".join(["An xpid (e.g. 'dv-0054-belenos@mary') or",
                                       "a piece of path to grab the experiment.",
                                       "Defaults to current working directory.",
                                       ]),
                                       nargs='?',
                                       default='.')
    parser.add_argument('-v', '--venv',
                        action='store_true',
                        help="Get path to the experiment venv's activate command.")
    args = parser.parse_args()
    this_xp = XP(args.experiment)
    if args.venv:
        print(this_xp.venv_activate)
    else:
        print(this_xp.xp_path)

