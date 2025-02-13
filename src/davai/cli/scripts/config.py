#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Show current DAVAI-env configuration.
"""

import argparse

from ..util import show_config

__all__ = ['main']


def main():
    args = get_args()
    if args.action == "show":
        show_config()

def get_args():
    parser = argparse.ArgumentParser(description="Show current DAVAI-env configuration.")
    parser.add_argument('action',
                        choices=['show', ],
                        nargs='?',
                        default='show')
    return parser.parse_args()

