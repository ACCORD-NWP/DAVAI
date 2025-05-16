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
import venv
import shutil

from ial_build.bundle import IALBundle, TmpIALbundleRepo

from .. import __version__
from ..util import gmkpack_build_job
from . import config
from . import DAVAI_HOST, DAVAI_XPID_SYNTAX, DAVAI_XP_COUNTER, DAVAI_XPID_RE, usecases, vapp
from .util import expandpath, set_default_mtooldir, vconf2usecase, usecase2vconf, initialized


class XPmaker(object):

    experiments_rootdir = os.path.realpath(expandpath(config['paths']['experiments']))

    @staticmethod
    def _next_xp_num():
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
    def _new_XP_path(cls, host, usecase):
        xpid = DAVAI_XPID_SYNTAX.format(xpid_num=cls._next_xp_num(),
                                        host=host,
                                        user=getpass.getuser())
        xp_path = cls.xp_path(xpid, usecase)
        assert not os.path.exists(xp_path), "XP path: '{}' already exists".format(xp_path)
        os.makedirs(xp_path)
        print("XP path created : {}".format(xp_path))
        return xp_path

    @classmethod
    def xp_path(cls, xpid, usecase):
        return os.path.join(cls.experiments_rootdir, xpid, vapp, usecase2vconf(usecase))

    @classmethod
    def new_xp(cls,
               sources_to_test,
               editable=False,
               davai_version=None,
               davai_remote_repo=config['defaults']['davai_remote_repo'],
               usecase=config['defaults']['usecase'],
               host=DAVAI_HOST,
               genesis_commandline=None,
               bundle_src_dir=None):
        """
        Create a new experiment.

        :param sources_to_test: information about the sources to be tested, provided as a dict
        :param editable: whether davai sources must be editable or not
        :param davai_version: version of the DAVAI to be used. If not provided, try to guess from IAL repo
        :param davai_remote_repo: origin repository of the DAVAI to be cloned
        :param usecase: type of set of tests to be prepared
        :param host: host machine
        :param genesis_commandline: command-line that was used to generate the experiment, to be saved in it
        :param bundle_src_dir: in case davai_version is not specified:
            cache directory where to download/update bundle repositories,
            in search for the davai_version, potentially stored in IAL.
        """

        assert usecase in usecases, "Usecase not implemented yet: " + usecase
        xp_path = cls._new_XP_path(host, usecase)
        # now XP path is created, we move in for the continuation of the experiment setup
        xp = XP(xp_path)
        xp.setup(sources_to_test,
                 editable=editable,
                 davai_version=davai_version,
                 davai_remote_repo=davai_remote_repo,
                 usecase=usecase,
                 host=host,
                 bundle_src_dir=bundle_src_dir)
        if genesis_commandline:
            xp.write_genesis(genesis_commandline)
        return xp


class XP(object):
    """Handles a Davai experiment."""

    davai_repo_name = 'DAVAI'
    sources_to_test_filename = os.path.join('conf', 'sources.yaml')
    sources_to_test_minimal_keys = (set(('IAL_git_ref',)),
                                    set(('IAL_bundle_ref', 'IAL_bundle_repository')),
                                    set(('IAL_bundle_file',))
                                    )
    davai_version_file_in_IAL = '.davai_default_version'
    venv_dir = 'venv'

    def __init__(self, xpid_or_path='.'):
        """
        Handles a Davai experiment.

        :param xpid_or_path: an xpid or a path to grab the experiment
        """
        self._retrieve_xp_path(xpid_or_path)
        # retrieve attributes
        self.xpid = os.path.basename(os.path.dirname(os.path.dirname(self.xp_path)))
        self.vapp = os.path.basename(os.path.dirname(self.xp_path))
        self.vconf = os.path.basename(self.xp_path)
        self.usecase = vconf2usecase(self.vconf)
        # build attributes
        self.general_config_file = os.path.join('conf','{}_{}.ini'.format(self.vapp, self.vconf))
        self.venv_path = os.path.join(self.xp_path, self.venv_dir)
        self.venv_python = os.path.join(self.venv_path, 'bin', 'python')
        self.venv_activate = os.path.join(self.venv_path, 'bin', 'activate')
        self.davai_repo_absdir = os.path.join(self.xp_path, self.davai_repo_name)
        self.sources_to_test_path = os.path.join(self.xp_path, os.path.join('conf', 'sources.yaml'))
        # checks
        assert self.vapp == 'davai', "Unknown vapp: '{}'.".format(self.vapp)
        assert self.usecase in usecases, "Unknown usecase: '{}'.".format(self.usecase)

    @property
    def _venv_site_path(self):
        return os.path.join(self.venv_path,
                            'lib',
                            'python{}.{}'.format(sys.version_info.major, sys.version_info.minor),
                            'site-packages')

    def _retrieve_xp_path(self, xpid_or_path):
        """Retrieve xp_path from an XPID or a piece of path."""
        if DAVAI_XPID_RE.match(xpid_or_path):
            xpid = xpid_or_path
        else:
            if xpid_or_path == '.':
                path = os.path.realpath(os.getcwd())
            else:
                assert os.path.exists(xpid_or_path), "This path does not exist: {}".format(xpid_or_path)
                path = os.path.realpath(os.path.abspath(xpid_or_path))
            rootlen = len(XPmaker.experiments_rootdir) + 1
            assert path.startswith(XPmaker.experiments_rootdir) and len(path) > rootlen, \
                   "This is not a path to a davai experiment: {}".format(path)
            xpid = path[rootlen:].split(os.sep)[0]
        # retrieve xp_path from XPID
        for u in usecases:
            xp_path = XPmaker.xp_path(xpid, u)
            if os.path.exists(xp_path):
                self.xp_path = xp_path
                break
        assert hasattr(self, 'xp_path'), "No experiment was found for XPID: '{}'.".format(xpid_or_path)

# setup --------------------------------------------------------------------------------------------------------------

    def setup(self,
              sources_to_test,
              editable=False,
              davai_version=None,
              davai_remote_repo=config['defaults']['davai_remote_repo'],
              usecase=config['defaults']['usecase'],
              host=DAVAI_HOST,
              bundle_src_dir=None):
        """
        Setup the experiment as a venv (at creation time).

        :param sources_to_test: information about the sources to be tested, provided as a dict
        :param editable: whether davai sources must be editable or not
        :param davai_version: version of the DAVAI to be used. If not provided, try to guess from IAL repo
        :param davai_remote_repo: remote repository of the DAVAI to be cloned
        :param usecase: type of set of tests to be prepared
        :param host: host machine
        :param bundle_src_dir: in case davai_version is not specified:
            cache directory where to download/update bundle repositories,
            in search for the davai_version, potentially stored in IAL.
        """
        os.makedirs(os.path.join(self.xp_path, 'conf'))
        self._setup_conf_sources(sources_to_test)
        if davai_version is None:
            # this will fail if the version is not known in IAL
            davai_version = self.guess_davai_version(bundle_src_dir=bundle_src_dir)
        if editable:
            # set DAVAI repo
            self._setup_DAVAI_repo(davai_remote_repo, davai_version)
            self._setup_new_venv()
        else:
            # use existing venv of this version
            venv_path = os.path.join(expandpath(config['paths']['venvs']), davai_version)
            self._link_venv(venv_path)
        self._setup_packages()  # remaining, not on PyPI: vortex
        self._setup_logs()
        # configuration files
        self._setup_conf_usecase(editable)
        self._setup_conf_general(editable, host=host)
        self._setup_final_prompt()

    def guess_davai_version(self, bundle_src_dir=None):
        """Guess davai_version from IAL repo (potentially through bundle)."""
        if 'IAL_git_ref' in self.sources_to_test and 'IAL_repository' in self.sources_to_test:
            IAL_git_ref = self.sources_to_test['IAL_git_ref']
            IAL_repository = self.sources_to_test['IAL_repository']
        else:
            if 'IAL_bundle_file' in self.sources_to_test:
                bf = self.sources_to_test['IAL_bundle_file']
                bundle = IALBundle(bf)
            elif 'IAL_bundle_ref' in self.sources_to_test and 'IAL_bundle_repository' in self.sources_to_test:
                br = TmpIALbundleRepo(self.sources_to_test['IAL_bundle_repository'])
                bundle = br.get_bundle(self.sources_to_test['IAL_bundle_ref'], to_file='__tmp__')
            else:
                raise AttributeError(
                    "Unable to guess davai_version from bundle or IAL git_ref/repository. Please specify.")
            bundle.download(src_dir=bundle_src_dir)
            IAL_git_ref = bundle.projects['IAL']['version']
            IAL_repository = bundle.local_project_repo('IAL')
        try:
            out = subprocess.check_output(['git', 'show', '{}:{}'.format(IAL_git_ref,
                                                                         self.davai_version_file_in_IAL)],
                                          cwd=IAL_repository)
        except subprocess.CalledProcessError:
            raise ValueError(" ".join(["DAVAI version could not be guessed from"
                                       "IAL_git_ref='{}'. Please specify.".format(IAL_git_ref)]))
        return out.strip().decode()

    def _checkout_davai_tests(self, gitref):
        """Check that requested tests version exists, and switch to it."""
        remote = 'origin'
        remote_gitref = '{}/{}'.format(remote, gitref)
        branches = subprocess.check_output(['git', 'branch'],
                                           stderr=None,
                                           cwd=self.davai_repo_absdir
                                           ).decode('utf-8').split('\n')
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
                                      stdout=subprocess.DEVNULL,
                                      cwd=self.davai_repo_absdir)
            except subprocess.CalledProcessError:
                # A.no
                print("'{}' is not known in refs/heads/".format(gitref))
                # B: maybe it is a remote branch ?
                cmd = ['git', 'show-ref', '--verify', 'refs/remotes/{}/{}'.format(remote, gitref)]
                try:
                    subprocess.check_call(cmd,
                                          stderr=subprocess.DEVNULL,
                                          stdout=subprocess.DEVNULL,
                                          cwd=self.davai_repo_absdir)
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
            print("Switch DAVAI repo from current HEAD '{}' to '{}'".format(head, gitref))
            subprocess.check_call(['git', 'checkout', gitref, '-q'],
                                  cwd=self.davai_repo_absdir)

    def _setup_DAVAI_repo(self, remote, version):
        """Clone and checkout required version of the DAVAI."""
        subprocess.check_call(['git', 'clone', remote, self.davai_repo_absdir],
                              cwd=self.xp_path)
        subprocess.check_call(['git', 'fetch', 'origin', version, '-q'],
                              cwd=self.davai_repo_absdir)
        self._checkout_davai_tests(version)

    def check_sources_to_test(self, sources_to_test):
        assertion_test = any([s.issubset(set(sources_to_test.keys())) for s in self.sources_to_test_minimal_keys])
        assertion_errmsg = "The set of keys in 'sources_to_test' should contain one of: {}".format(
                           self.sources_to_test_minimal_keys)
        assert assertion_test, assertion_errmsg

    def _link_venv(self, venv_path):
        """Link venv to an existing venv path."""
        print("Using venv:", venv_path)
        os.symlink(venv_path, self.venv_path)

    def _setup_new_venv(self):
        """Create a new venv in the XP."""
        # create venv within the xp
        print("Create virtualenv ({})...".format(self.venv_path))
        venv.create(self.venv_path,
                    with_pip=True,
                    symlinks=False,
                    prompt='venv@davai:{}'.format(self.xpid))
        print("... virtualenv created.")
        # install DAVAI and dependencies in the venv
        print("Setup virtualenv...")
        subprocess.check_call([self.venv_python, '-m', 'pip', 'install', '-e', self.davai_repo_absdir])
        print("... virtualenv set up.")

    def _setup_conf_sources(self, sources_to_test):
        """Sources config: information on sources to be tested."""
        self.check_sources_to_test(sources_to_test)
        with io.open(self.sources_to_test_path, 'w') as f:
            yaml.dump(sources_to_test, f)

    def _setup_conf_usecase(self, editable):
        """Usecase config : set of jobs/tests."""
        basename = '{}.yaml'.format(self.usecase)
        loc = os.path.join(self.xp_path, 'conf', basename)
        if editable:
            target = os.path.join('..', self.davai_repo_name, 'src', 'tasks', 'conf', basename)
            os.symlink(target, loc)
        else:
            target = os.path.join(self._venv_site_path, 'tasks', 'conf', basename)
            bak = loc + '.bak'
            os.symlink(target, bak)
            shutil.copyfile(target, loc)

    def _setup_conf_general(self, editable, host=DAVAI_HOST):
        """General config file for the jobs."""
        basename = '{}.ini'.format(host)
        loc = os.path.join(self.xp_path, self.general_config_file)
        if editable:
            target = os.path.join('..', self.davai_repo_name, 'src', 'tasks', 'conf', basename)
            os.symlink(target, loc)
        else:
            target = os.path.join(self._venv_site_path, 'tasks', 'conf', basename)
            bak = loc + '.bak'
            os.symlink(target, bak)
            shutil.copyfile(target, loc)

    def _setup_packages(self):
        """Link necessary packages in XP."""
        packages = {p:expandpath(config['packages'][p]) for p in config['packages']}
        for package, path in packages.items():
            os.symlink(expandpath(path), os.path.join(self.xp_path, package))

    def _setup_logs(self):
        """Deport 'logs' directory."""
        logs_directory = expandpath(config['paths']['logs'])
        logs = os.path.join(logs_directory, self.xpid)
        os.makedirs(logs)
        os.symlink(logs, os.path.join(self.xp_path, 'logs'))

    def _setup_final_prompt(self):
        """Final prompt for the setup of the experiment."""
        print("-" * 80)
        print("DAVAI xp '{}' has been successfully setup in:".format(self.xpid))
        print("**", self.xp_path, "**")
        print("   -> XP config file: '{}'".format(self.general_config_file))
        print("   -> Activation venv: 'source {}/bin/activate'".format(self.venv_dir))
        print("   -> Run experiment : 'davai-run_xp'")
        print("-" * 80)

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

    def assert_valid_xp_path(self):
        """Assert that the xp_path is actually a davai experiment."""
        assert os.path.exists(os.path.join(self.xp_path, self.general_config_file)), \
               "This is not a davai experiment root directory: {}".format(self.xp_path)

    def assert_venv_python(self):
        """Assert the python running is the one from the experiment's venv."""
        sys_venv = os.path.realpath(os.path.split(sys.executable)[0])
        this_venv = os.path.realpath(os.path.join(self.venv_path, 'bin'))
        assert sys_venv == this_venv, \
               " ".join(["The python running is not the one of this experiment.",
                         "Load venv: 'source {}'.".format(self.venv_activate)])

    @property
    def conf(self):
        if not hasattr(self, '_conf'):
            config = configparser.ConfigParser()
            config.read(os.path.join(self.xp_path, self.general_config_file))
            self._conf = config
        return self._conf

    @property
    def sources_to_test(self):
        """Sources config: information on sources to be tested."""
        if not hasattr(self, '_sources_to_test'):
            with io.open(self.sources_to_test_path, 'r') as f:
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
                c['IAL_bundle_repository'] = c.get('IAL_bundle_repository', config['defaults']['IAL_bundle_repository'])
            self._sources_to_test = c
        return self._sources_to_test

    @property
    def all_jobs(self):
        """Get all jobs according to *usecase* (found in config)."""
        if not hasattr(self, '_all_jobs'):
            jobs_list_file = 'conf/{}.yaml'.format(self.usecase)
            with io.open(os.path.join(self.xp_path, jobs_list_file), 'r') as fin:
                self._all_jobs = yaml.load(fin, yaml.Loader)
        return self._all_jobs

    @property
    def davai_version(self):
        try:
            # editable case
            cmd = ['git', 'log' , '-n1', '--decorate']
            output = subprocess.check_output(cmd,
                                             cwd=self.davai_repo_absdir
                                             ).decode('utf-8').split('\n')
            return output[0]
        except Exception:
            # version from the venv
            return __version__

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
        mkjob = 'vortex/bin/mkjob.py'
        cmd = ['python3', mkjob, '-j',
               'task={}'.format(task.strip()),
               'testjob={}'.format(task.strip()),
               'name={}'.format(name.strip()),
               'python={}'.format(sys.executable)]
        cmd.extend(['{}={}'.format(k,v) for k,v in extra_parameters.items()])
        print("Executing: '{}'".format(' '.join(cmd)))
        if not drymode:
            subprocess.check_call(cmd, cwd=self.xp_path)

    def ciboulai_init(self):
        """(Re-)Initialize Ciboulai dashboard."""
        self._launch('ciboulai_xpsetup', 'ciboulai_xpsetup',
                     profile='rd',
                     usecase=self.usecase,
                     davai_version=self.davai_version.replace("'", '"'),
                     **self.sources_to_test)

    def build(self,
              drymode=False,
              skip_fetching_sources=False,
              fake_build=False,
              archive_as_ref=False,
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
                                       fake_build=fake_build,
                                       archive_as_ref=archive_as_ref)
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
            raise KeyError(msg.format(self.sources_to_test_filename))
        self._launch(build_job, 'build',
                     drymode=drymode,
                     profile='rd',  # interactive, not in batch/scheduler
                     preexisting_pack=preexisting_pack,
                     cleanpack=cleanpack,
                     **self.sources_to_test)

    def _gmkpack_launch_build(self,
                              drymode=False,
                              cleanpack=False,
                              fake_build=False,
                              archive_as_ref=False):
        """Launch build job."""
        os.environ['DAVAI_START_BUILD'] = str(time.time())
        # run build in batch/scheduler
        self._launch(gmkpack_build_job, 'build',
                     drymode=drymode,
                     cleanpack=cleanpack,
                     fake_build=fake_build,
                     archive_as_ref=archive_as_ref,
                     **self.sources_to_test)
        # run build monitoring (interactively)
        if DAVAI_HOST != 'atos_bologna':  # FIXME: dirty
            set_default_mtooldir()
        self._launch('build.wait4build', 'build',
                     drymode=drymode,
                     profile='rd')

    def launch_jobs(self,
                    only_job=None,
                    drymode=False,
                    mpiname=None,
                    archive_as_ref=False):
        """Launch jobs, either all, or only the one requested."""
        extra_params = {}
        if mpiname is not None:
            extra_params['mpiname'] = mpiname
        extra_params['archive_as_ref'] = archive_as_ref
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
        # TODO: transform into a task run in interactive (like ciboulai_init)
        # First we need MTOOLDIR set up for retrieving paths
        set_default_mtooldir()
        # Then set Vortex in path
        vortexpath = expandpath(config['packages']['vortex'])
        sys.path.extend([vortexpath, os.path.join(vortexpath, 'src'), os.path.join(vortexpath, 'site')])
        # vortex/davai
        import vortex
        from ..vtx.util import SummariesStack
        # process stack or task
        stack = SummariesStack(vortex.ticket(), self.vapp, self.vconf, self.xpid)
        if task is None:
            stack.tasks_status(print_it=True)
        else:
            stack.task_summary_fullpath(task)

