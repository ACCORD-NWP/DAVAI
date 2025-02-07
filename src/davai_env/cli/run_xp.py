#!/usr/bin/env python3
# -*- coding:Utf-8 -*-

import argparse

from ..experiment import XP

__all__ = ['main']


def main():
    args = get_args()
    this_xp = XP(args.experiment)
    this_xp.ciboulai_init()
    # build
    this_xp.build(
                  skip_fetching_sources=args.skip_fetching_sources,
                  drymode=args.drymode,
                  # gmkpack arguments
                  preexisting_pack=args.preexisting_pack,
                  cleanpack=args.cleanpack,
                  )
    # run_tests
    this_xp.launch_jobs(only_job=args.only_job,
                        drymode=args.drymode,
                        mpiname=args.mpiname)
    this_xp.afterlaunch_prompt()


def get_args():
    parser = argparse.ArgumentParser(description='Run experiment: ciboulai_init, build, run_tests. To be executed from the XP directory !')
    parser.add_argument('experiment',
                        help=" ".join(["An xpid (e.g. 'dv-0054-belenos@mary') or",
                                       "a piece of path to grab the experiment.",
                                       "Defaults to current working directory.",
                                       ]),
                                       nargs='?',
                                       default='.')
    parser.add_argument('--drymode',
                        action='store_true',
                        help="Dry mode: print commands to be executed, but do not run them")
    # build arguments
    parser.add_argument('-s', '--skip_fetching_sources',
                        action='store_true',
                        help="Skip fetching the sources (assuming they have been fetched / and pack preexists for gmkpack).")
    parser.add_argument('-e', '--preexisting_pack',
                        action='store_true',
                        help="Gmkpack: assume the pack already preexists, and repopulate it with sources changes.")
    parser.add_argument('-c', '--cleanpack',
                        action='store_true',
                        help="Gmkpack: clean pack before git2pack+pack2bin.")
    # run_tests arguments
    parser.add_argument('-j', '--only_job',
                        default=None,
                        help="Restrict the launch to the given job only (which may contain several tests)")
    parser.add_argument('--mpiname',
                        default=None,
                        help="MPI launcher, as listed in vortex (e.g. 'srun', 'mpirun', 'srun-ddt'.")
    return parser.parse_args()

