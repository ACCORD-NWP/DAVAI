#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

import argparse

from ..experiment import XP

__all__ = ['main']


def main():

    parser = argparse.ArgumentParser(description='Check if the current working directory is an experiment. ' +
                                                 'Return the name of the experiment if so (and not silent mode).')
    parser.add_argument('-s', '--silent',
                        action='store_true',
                        help="Silent mode")
    args = parser.parse_args()
    this_xp = XP()
    if not args.silent:
        print(this_xp.xpid)

