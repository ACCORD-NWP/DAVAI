#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

import argparse

from ..experiment import XP

__all__ = ['main']

def main():
    parser = argparse.ArgumentParser(description="(Re-)Initialize experiment in Ciboulai dashboard server. " +
                                                 "To be executed from the XP directory !")
    parser.add_argument('experiment',
                        help=" ".join(["An xpid (e.g. 'dv-0054-belenos@mary') or",
                                       "a piece of path to grab the experiment.",
                                       "Defaults to current working directory.",
                                       ]),
                                       nargs='?',
                                       default='.')
    args = parser.parse_args()
    this_xp = XP(args.experiment)
    this_xp.assert_venv_python()
    this_xp.ciboulai_init()

