#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Create a Davai experiment to test an IAL Git reference.
"""

import os
import argparse
import sys

from .. import config, DAVAI_HOST
from ..experiment import XPmaker
from ..util import expandpath

__all__ = ['main']


def main():

    # get args
    args = get_args()

    # create new experiment
    XPmaker.new_xp(args.sources_to_test,
                   editable=args.editable,
                   davai_tests_version=args.davai_tests_version,
                   davai_tests_origin=args.davai_tests_origin,
                   usecase=args.usecase,
                   host=args.host,
                   genesis_commandline=" ".join(sys.argv))


def get_args():

    parser = argparse.ArgumentParser(description='Create a Davai experiment to test an IAL Git reference.')
    parser.add_argument('IAL_git_ref',
                        help="IAL Git reference to be tested. Can be a branch, a tag or a commit number.")
    parser.add_argument('-e', '--editable',
                        action='store_true',
                        help="Editable: use an editable version of Davai sources (hence a brand new venv).")
    parser.add_argument('-r', '--IAL_repo',
                        default=expandpath(config['paths']['IAL_repository']),
                        dest='IAL_repository',
                        help=" ".join([
                            "Path to IAL Git repository in which to find 'IAL_git_ref' argument.",
                            "Default ({})".format(config['paths']['IAL_repository']),
                            "can be set through section [paths] of user config file"]))
    parser.add_argument('-v', '--tests_version',
                        dest='davai_tests_version',
                        help="Version of the Davai test bench to be used.")
    parser.add_argument('-c', '--comment',
                        default=None,
                        help="Comment about experiment. Defaults to IAL_git_ref, IAL_bundle or IAL_bundle_file.")
    parser.add_argument('-u', '--usecase',
                        default=config['defaults']['usecase'],
                        help="Usecase: NRV (restrained set of canonical tests) or ELP (extended elementary tests); " +
                             "More (PC, ...) to come. Defaults to: '{}'".format(config['defaults']['usecase']))
    parser.add_argument('--origin', '--davai_tests_origin',
                        default=config['defaults']['davai_tests_origin'],
                        dest='davai_tests_origin',
                        help=("URL of the DAVAI-tests origin repository to be cloned in XP. " +
                              "Default ({}) can be set through section [defaults] " +
                              "of user config file").format(config['defaults']['davai_tests_origin']))
    parser.add_argument('--host',
                        default=DAVAI_HOST,
                        help="Generic name of host machine, in order to find paths to necessary packages. " +
                             ("Default is guessed ({}), or can be set through " +
                              "section 'hosts' of user config file").format(DAVAI_HOST))
    args = parser.parse_args()
    # pre-process args
    args.sources_to_test = dict(IAL_git_ref=args.IAL_git_ref,
                                IAL_repository=os.path.abspath(args.IAL_repository),
                                comment=args.comment)
    return args

