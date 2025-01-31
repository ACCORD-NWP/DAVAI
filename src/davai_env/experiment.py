#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handle a Davai experiment.
"""

import sys
import os
import getpass
import io
import re
import subprocess
import configparser
import yaml
import time

from . import config, guess_host, initialized
from . import DAVAI_XPID_SYNTAX, DAVAI_XP_COUNTER
from .util import expandpath, set_default_mtooldir, vconf2usecase, usecase2vconf

initialized()


class XPmaker(object):

    experiments_rootdir = expandpath(config['paths']['experiments'])

    @staticmethod
    def next_xp_num():
        """Get number of next Experiment."""
        if not os.path.exists(DAVAI_XP_COUNTER):
            num = 0
        else:
            with io.open(DAVAI_XP_COUNTER, 'r') as f:
                num = int(f.readline())
        next_num = num + 1
        with io.open(DAVAI_XP_COUNTER, 'w') as f:
            f.write(str(next_num))
        return next_num

    @classmethod
    def _new_XPID(cls, host):
        return DAVAI_XPID_SYNTAX.format(xpid_num=cls.next_xp_num(),
                                        host=host,
                                        user=getpass.getuser())

    @classmethod
    def _new_XP_path(cls, host, usecase):
        return os.path.join(cls.experiments_rootdir, cls._new_XPID(host), 'davai', usecase2vconf(usecase))

    @staticmethod
    def _setup_XP_path(xp_path):
        assert not os.path.exists(xp_path), "XP path: '{}' already exists".format(xp_path)
        os.makedirs(xp_path)
        print("XP path created : {}".format(xp_path))

    @classmethod
    def new_xp(cls, sources_to_test, davai_tests_version,
               davai_tests_origin=config['defaults']['davai_tests_origin'],
               usecase=config['defaults']['usecase'],
               host=guess_host(),
               genesis_commandline=None):
        """
        Create a new experiment.

        :param sources_to_test: information about the sources to be tested, provided as a dict
        :param davai_tests_version: version of the DAVAI-tests to be used
        :param davai_tests_origin: origin repository of the DAVAI-tests to be cloned
        :param usecase: type of set of tests to be prepared
        :param host: host machine
        :param genesis_commandline: command-line that was used to generate the experiment, to be saved in it
        """

        assert usecase in ('NRV', 'ELP'), "Usecase not implemented yet: " + usecase
        xp_path = cls._new_XP_path(host, usecase)
        cls._setup_XP_path(xp_path)
        # now XP path is created, we move in for the continuation of the experiment setup
        os.chdir(xp_path)
        xp = ThisXP(new=True)
        xp.setup(sources_to_test, davai_tests_version,
                 davai_tests_origin=davai_tests_origin,
                 usecase=usecase,
                 host=host)
        if genesis_commandline:
            xp.write_genesis(genesis_commandline)
        return xp


class ThisXP(object):
    """Handles the existing experiment determined by the current working directory."""

    davai_tests_dir = 'DAVAI-tests'
    sources_to_test_file = os.path.join('conf', 'sources.yaml')
    sources_to_test_minimal_keys = (set(('IAL_git_ref',)),
                                    set(('IAL_bundle_ref', 'IAL_bundle_repository')),
                                    set(('IAL_bundle_file',))
                                    )

    def __init__(self, new=False):
        self.xp_path = os.getcwd()
        self.xpid = os.path.basename(os.path.dirname(os.path.dirname(self.xp_path)))
        self.vapp = os.path.basename(os.path.dirname(self.xp_path))
        self.vconf = os.path.basename(self.xp_path)
        self.usecase = vconf2usecase(self.vconf)
        self.general_config_file = os.path.join('conf','{}_{}.ini'.format(self.vapp, self.vconf))
        if not new:
            self.assert_cwd_is_an_xp()

# setup --------------------------------------------------------------------------------------------------------------

    def setup(self, sources_to_test, davai_tests_version,
              davai_tests_origin=config['defaults']['davai_tests_origin'],
              usecase=config['defaults']['usecase'],
              host=guess_host()):
        """
        Setup the experiment (at creation time).

        :param sources_to_test: information about the sources to be tested, provided as a dict
        :param davai_tests_version: version of the DAVAI-tests to be used
        :param davai_tests_origin: remote repository of the DAVAI-tests to be cloned
        :param usecase: type of set of tests to be prepared
        :param host: host machine
        """
        # set DAVAI-tests repo
        self._setup_DAVAI_tests(davai_tests_origin, davai_tests_version)
        self._setup_tasks()
        self._setup_packages()
        self._setup_logs()
        # configuration files
        os.makedirs('conf')
        self._setup_conf_sources(sources_to_test)
        self._setup_conf_usecase(usecase)
        self._setup_conf_general(host)
        self._setup_final_prompt()

    @staticmethod
    def _checkout_davai_tests(gitref):
        """Check that requested tests version exists, and switch to it."""
        remote = 'origin'
        remote_gitref = '{}/{}'.format(remote, gitref)
        branches = subprocess.check_output(['git', 'branch'], stderr=None).decode('utf-8').split('\n')
        head = [line.strip() for line in branches if line.startswith('*')][0][2:]
        detached = re.match('\(HEAD detached at (?P<ref>.*)\)$', head)
        if detached:
            head = detached.group('ref')
        if (head != gitref and head != remote_gitref) or (head == gitref and remote):
            # determine if required tests version is a branch or not
            try:
                # A: is it a local branch ?
                cmd = ['git', 'show-ref', '--verify', 'refs/heads/{}'.format(gitref)]
                subprocess.check_call(cmd,
                                      stderr=subprocess.DEVNULL,
                                      stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                # A.no
                print("'{}' is not known in refs/heads/".format(gitref))
                # B: maybe it is a remote branch ?
                cmd = ['git', 'show-ref', '--verify', 'refs/remotes/{}/{}'.format(remote, gitref)]
                try:
                    subprocess.check_call(cmd,
                                          stderr=subprocess.DEVNULL,
                                          stdout=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    # B.no: so either it is tag/commit, or doesn't exist, nothing to do about remote
                    print("'{}' is not known in refs/remotes/{}".format(gitref, remote))
                else:
                    # B.yes: remote branch only                        gitref = remote_gitref
                    gitref = remote_gitref
                    print("'{}' taken from remote '{}'".format(gitref, remote))
            else:
                # A.yes: this is a local branch, do we take it from remote or local ?
                gitref = remote_gitref
            # remote question has been sorted
            print("Switch DAVAI-tests repo from current HEAD '{}' to '{}'".format(head, gitref))
            try:
                subprocess.check_call(['git', 'checkout', gitref, '-q'])
            except subprocess.CalledProcessError:
                print("Have you updated your DAVAI-tests repository (command: davai-update) ?")
                raise

    def _setup_DAVAI_tests(self, remote, version):
        """Clone and checkout required version of the DAVAI-tests."""
        subprocess.check_call(['git', 'clone', remote, self.davai_tests_dir])
        os.chdir(self.davai_tests_dir)
        subprocess.check_call(['git', 'fetch', 'origin', version, '-q'])
        self._checkout_davai_tests(version)
        os.chdir(self.xp_path)

    def check_sources_to_test(self, sources_to_test):
        assertion_test = any([s.issubset(set(sources_to_test.keys())) for s in self.sources_to_test_minimal_keys])
        assertion_errmsg = "The set of keys in 'sources_to_test' should contain one of: {}".format(
                           self.sources_to_test_minimal_keys)
        assert assertion_test, assertion_errmsg

    def _setup_conf_sources(self, sources_to_test):
        """Sources config: information on sources to be tested."""
        self.check_sources_to_test(sources_to_test)
        with io.open(self.sources_to_test_file, 'w') as f:
            yaml.dump(sources_to_test, f)

    def _setup_conf_usecase(self, usecase):
        """Usecase config : set of jobs/tests."""
        filename = os.path.join('conf', '{}.yaml'.format(self.usecase))
        os.symlink(os.path.join('..', self.davai_tests_dir, filename),
                   filename)

    def _setup_conf_general(self, host=guess_host()):
        """General config file for the jobs."""
        host_general_config_file = os.path.join('..', self.davai_tests_dir, 'conf', '{}.ini'.format(host))
        os.symlink(host_general_config_file,
                   self.general_config_file)

    def _setup_tasks(self):
        """Link tasks."""
        os.symlink(os.path.join(self.davai_tests_dir, 'src', 'tasks'),
                   'tasks')

    def _setup_packages(self):
        """Link necessary packages in XP."""
        # davai_taskutil from DAVAI-tests locally checkedout
        os.symlink(os.path.join(self.davai_tests_dir, 'src', 'davai_taskutil'),
                   'davai_taskutil')
        # other packages
        packages = {p:expandpath(config['packages'][p]) for p in config['packages']}
        for package, path in packages.items():
            os.symlink(expandpath(path), package)

    def _setup_logs(self):
        """Deport 'logs' directory."""
        logs_directory = expandpath(config['paths']['logs'])
        logs = os.path.join(logs_directory, self.xpid)
        os.makedirs(logs)
        os.symlink(logs, 'logs')

    def _setup_final_prompt(self):
        """Final prompt for the setup of the experiment."""
        print("------------------------------------")
        print("DAVAI xp '{}' has been successfully setup !".format(self.xpid))
        print("Now go to the XP path below and:")
        print("- if necessary, tune experiment in '{}'".format(self.general_config_file))
        print("- run experiment using: 'davai-run_xp'")
        print("  =>", self.xp_path)
        print("------------------------------------")

    def write_genesis(self, command):
        """Write the command that created the XP in a .genesis file."""
        with io.open(os.path.join(self.xp_path, '.genesis'), 'w') as g:
            g.write(str(command))

# properties ----------------------------------------------------------------------------------------------------------

    def cwd_is_an_xp(self):
        """Whether the cwd is an actual experiment or not."""
        return os.path.exists(self.general_config_file)

    def assert_cwd_is_an_xp(self):
        """Assert that the cwd is an actual experiment."""
        assert self.cwd_is_an_xp(), "Current working directory is not a Davai experiment directory"

    @property
    def conf(self):
        if not hasattr(self, '_conf'):
            config = configparser.ConfigParser()
            config.read(self.general_config_file)
            self._conf = config
        return self._conf

    @property
    def sources_to_test(self):
        """Sources config: information on sources to be tested."""
        if not hasattr(self, '_sources_to_test'):
            with io.open(self.sources_to_test_file, 'r') as f:
                c = yaml.load(f, yaml.Loader)
            self.check_sources_to_test(c)
            # complete particular config
            if 'IAL_git_ref' in c:
                # sources to be tested taken from IAL_git_ref@IAL_repository
                if c.get('comment', None) is None:
                    c['comment'] = c['IAL_git_ref']
                repo = c.get('IAL_repository', config['paths']['IAL_repository'])
                c['IAL_repository'] = expandpath(repo)
            elif 'IAL_bundle_file' in c:
                # sources to be tested taken from an IAL bundle file
                if c.get('comment', None) is None:
                    c['comment'] = c['IAL_bundle_file']
            elif 'IAL_bundle_ref' in c:
                # sources to be tested taken from IAL_bundle_ref@IAL_bundle_repository
                if c.get('comment', None) is None:
                    c['comment'] = c['IAL_bundle_ref']
                c['IAL_bundle_repository'] = c.get('IAL_bundle_repository', config['default']['IAL_bundle_repository'])
            self._sources_to_test = c
        return self._sources_to_test

    @property
    def all_jobs(self):
        """Get all jobs according to *usecase* (found in config)."""
        if not hasattr(self, '_all_jobs'):
            jobs_list_file = 'conf/{}.yaml'.format(self.usecase)
            with io.open(jobs_list_file, 'r') as fin:
                self._all_jobs = yaml.load(fin, yaml.Loader)
        return self._all_jobs

    @property
    def davai_tests_version(self):
        cmd = ['git', 'log' , '-n1', '--decorate']
        output = subprocess.check_output(cmd,
                                         cwd=os.path.join(self.xp_path, self.davai_tests_dir)
                                         ).decode('utf-8').split('\n')
        return output[0]

# utilities ----------------------------------------------------------------------------------------------------------

    def print_jobs(self):
        """Print all jobs according to *usecase* (found in config)."""
        for family, jobs in self.all_jobs.items():
            for job in jobs:
                print('.'.join([family, job]))

    def _launch(self, task, name,
               drymode=False,
               **extra_parameters):
        """
        Launch one job.

        :param task: submodule of the driver to be executed, e.g. assim.BSM_4D_arpege
        :param name: name of the job, to get its confog characteristics (profile, ...)
        :param extra_parameters: extra parameters to be passed to mkjob on the fly
        """
        cmd = ['python3', 'vortex/bin/mkjob.py', '-j',
               'task={}'.format(task.strip()),
               'name={}'.format(name.strip()),
               'python={}'.format(sys.executable)]
        cmd.extend(['{}={}'.format(k,v) for k,v in extra_parameters.items()])
        print("Executing: '{}'".format(' '.join(cmd)))
        if not drymode:
            subprocess.check_call(cmd)

    def ciboulai_init(self):
        """(Re-)Initialize Ciboulai dashboard."""
        self._launch('ciboulai_xpsetup', 'ciboulai_xpsetup',
                     profile='rd',
                     usecase=self.usecase,
                     tests_version=self.davai_tests_version.replace("'", '"'),
                     **self.sources_to_test)

    def build(self,
              drymode=False,
              skip_fetching_sources=False,
              fake_build=False,
              # gmkpack arguments
              preexisting_pack=False,
              cleanpack=False):
        """Generic, main davai build of executables."""
        compiling_system = self.conf['DEFAULT']['compiling_system']
        if compiling_system == 'gmkpack':
            if not skip_fetching_sources:
                # fetch sources (interactively)
                self._gmkpack_fetch_sources(drymode=drymode,
                                            preexisting_pack=preexisting_pack,
                                            cleanpack=cleanpack)
            # launch build in batch/scheduler
            self._gmkpack_launch_build(drymode=drymode,
                                       cleanpack=cleanpack,
                                       fake_build=fake_build)
        else:
            raise NotImplementedError("compiling_system == {}".format(compiling_system))

    def _gmkpack_fetch_sources(self,
                               drymode=False,
                               preexisting_pack=False,
                               cleanpack=False):
        """Fetch sources for build with gmkpack."""
        if 'IAL_git_ref' in self.sources_to_test:
            # build from a single IAL Git reference
            build_job = 'build.gmkpack.gitref2pack'
        elif any([k in self.sources_to_test for k in ['IAL_bundle_ref', 'IAL_bundle_file']]):
            # build from a bundle
            build_job = 'build.gmkpack.bundle2pack'
        else:
            msg = "Config file '{}' should contain one of: ('IAL_git_ref', 'IAL_bundle_ref', 'IAL_bundle_file')"
            raise KeyError(msg.format(self.sources_to_test_file))
        self._launch(build_job, 'build',
                     drymode=drymode,
                     profile='rd',  # interactive, not in batch/scheduler
                     preexisting_pack=preexisting_pack,
                     cleanpack=cleanpack,
                     **self.sources_to_test)

    def _gmkpack_launch_build(self,
                              drymode=False,
                              cleanpack=False,
                              fake_build=False):
        """Launch build job."""
        os.environ['DAVAI_START_BUILD'] = str(time.time())
        # run build in batch/scheduler
        build_job = 'build.gmkpack.pack2bin'
        self._launch(build_job, 'build',
                     drymode=drymode,
                     cleanpack=cleanpack,
                     fake_build=fake_build,
                     **self.sources_to_test)
        # run build monitoring (interactively)
        if guess_host() != 'atos_bologna':  # FIXME: dirty
            set_default_mtooldir()
        self._launch('build.wait4build', 'build',
                     drymode=drymode,
                     profile='rd')

    def launch_jobs(self, only_job=None, drymode=False, mpiname=None):
        """Launch jobs, either all, or only the one requested."""
        extra_params = {}
        if mpiname is not None:
            extra_params['mpiname'] = mpiname
        only_job_launched = False
        for family, jobs in self.all_jobs.items():
            for job in jobs:
                task = '.'.join([family, job])
                name = job
                if only_job in (None, task):
                    self._launch(task, name, drymode=drymode, **extra_params)
                    if only_job is not None:
                        only_job_launched = True
        if only_job is not None and not only_job_launched:
            raise ValueError("Unknown job: {}".format(only_job))

    def afterlaunch_prompt(self):
        print("=" * 100)
        print("=== {:^92} ===".format("DAVAI {} test bench launched through job scheduler !".format(self.usecase)))
        print("=== {:^92} ===".format("Checkout Ciboulai for results on: {}".format(self.conf['DEFAULT']['davai_server'])))
        print("=" * 100)

    def status(self, task=None):
        """Print status of tasks, read from cache files."""
        # First we need MTOOLDIR set up for retrieving paths
        set_default_mtooldir()
        # Then set Vortex in path
        vortexpath = expandpath(config['packages']['vortex'])
        sys.path.extend([vortexpath, os.path.join(vortexpath, 'src'), os.path.join(vortexpath, 'site')])
        # vortex/davai
        import vortex
        import davai
        # process stack or task
        stack = davai.util.SummariesStack(vortex.ticket(), self.vapp, self.vconf, self.xpid)
        if task is None:
            stack.tasks_status(print_it=True)
        else:
            stack.task_summary_fullpath(task)

