#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

import argparse

from ..experiment import XP

__all__ = ['main']


def main():
    parser = argparse.ArgumentParser(description='Prints the version of tests currently in use in this experiment.')
    parser.add_argument('experiment',
                        help=" ".join(["An xpid (e.g. 'dv-0054-belenos@mary') or",
                                       "a piece of path to grab the experiment.",
                                       "Defaults to current working directory.",
                                       ]),
                                       nargs='?',
                                       default='.')
    parser.parse_args()
    this_xp = XP(args.experiment)
    print(this_xp.davai_version)

