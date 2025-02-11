#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Show current DAVAI-env configuration, or provide a commented user config template, if not existing.
"""

import argparse

from .. import show_config, preset_user_config_file

__all__ = ['main']


def main():
    args = get_args()
    if args.action == "show":
        show_config()
    else:
        preset_user_config_file(prompt=True)

def get_args():
    parser = argparse.ArgumentParser(description="Show current DAVAI-env configuration, " +
                                                 "or provide a commented user config template, if not existing.")
    parser.add_argument('action',
                        choices=['show', 'preset_user'])
    return parser.parse_args()

