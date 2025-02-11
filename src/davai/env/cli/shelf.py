#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
A shelf is a Vortex pseudo-experiment in which are stored input data as in a Vortex experiment.
This tool helps to move shelves between archive, marketplace cache and tarfiles.
"""

import os
import sys
import argparse

from ..shelf import Shelf

__all__ = ['main']


def main():
    args = get_args()
    shelf = Shelf(args.shelf)
    getattr(shelf, args.action)(**vars(args))

def get_args():
    parser = argparse.ArgumentParser(description='Move shelves between archive, marketplace cache and tarfiles.')
    parser.add_argument('action',
                        choices=['mkt2arch', 'mkt2tar', 'tar2mkt', 'arch2mkt', 'arch_prestage'],
                        help='action to realise on shelves')
    parser.add_argument('shelf',
                        help="shelf name (filename including .tar/.tgz if action is 'tar2mkt')")
    parser.add_argument('-a', '--archive',
                        help='archive machine name')
    parser.add_argument('-d', '--out_dir',
                        help="directory in which to output tarfile if action is 'mkt2tar'. " +
                             "Defaults to current directory")
    parser.add_argument('-z', '--gz_compression',
                        action='store_true',
                        default=False,
                        help='activate gz compression in tarfile export')
    args = parser.parse_args()
    if 'arch' in args.action:
        assert args.archive is not None, "archive argument (-a) must be provided with action: '{}'".format(args.action)
    return args

