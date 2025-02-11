#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

import argparse

from ..experiment import XP

__all__ = ['main']


def main():

    args = get_args()

    this_xp = XP(args.experiment)
    this_xp.assert_venv_python()
    if args.list_jobs:
        this_xp.print_jobs()
    else:
        this_xp.launch_jobs(only_job=args.only_job,
                            drymode=args.drymode,
                            mpiname=args.mpiname)
        this_xp.afterlaunch_prompt()

def get_args():
    parser = argparse.ArgumentParser(description='Launch tests. To be ran from the XP directory only !')
    parser.add_argument('experiment',
                        help=" ".join(["An xpid (e.g. 'dv-0054-belenos@mary') or",
                                       "a piece of path to grab the experiment.",
                                       "Defaults to current working directory.",
                                       ]),
                                       nargs='?',
                                       default='.')
    parser.add_argument('-j', '--only_job',
                        default=None,
                        help="Restrict the launch to the given job only (which may contain several tests)")
    parser.add_argument('-l', '--list_jobs',
                        action='store_true',
                        help="List the jobs supposed to be launched")
    parser.add_argument('--mpiname',
                        default=None,
                        help="MPI launcher, as listed in vortex (e.g. 'srun', 'mpirun', 'srun-ddt'.")
    parser.add_argument('--drymode',
                        action='store_true',
                        help="Dry mode: print commands to be executed, but do not run them")
    return parser.parse_args()

