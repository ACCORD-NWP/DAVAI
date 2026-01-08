# -*- coding: utf-8 -*-
from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task

from davai.vtx.tasks.mixins import DavaiTaskMixin, BundleMixin
from davai.vtx.algo.build import binaries_syntax_in_workdir

import os

class BundleInstall(Task, DavaiTaskMixin, BundleMixin):

    experts = [FPDict({'kind':'bundle_install'}),]
    _taskinfo_kind = 'statictaskinfo'

    @property
    def programs(self):
        """List of programs to be compiled (may depend on flavour)."""
        if  self.conf.get("programs_by_flavour",False):
            programs = self.conf.programs_by_flavour.get(self.conf.compilation_flavour, self.conf.default_programs)
        else:
            programs=self.conf.default_programs
        if isinstance(programs, list):
            programs = ','.join(programs)  # because Algo's footprint attribute expect a str
        return programs

    def process(self):
        # self._set_gmkpack_env()
        self.tasks2wait4_add()  # warn wait4build manager to wait for this task
        self._wrapped_init()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.2/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                threads     = self.conf.get("threads"),
                programs    = self.programs,
                build_dir   = self.bundle_xp_build_dir,
                bundle_dir = self.bundle_dir,
                bundle_src_dir  = self.bundle_src_dir,
                reconfigure_build = self.conf.get("reconfigure_build"),
                clean_build        = self.conf.get("clean_build"),
                ninja        = self.conf.get("ninja"),
                fake_build     = self.conf.get('fake_build', False),
                flavour        = self.conf.compilation_flavour,
                platform        = self.conf.compilation_platform,
                crash_witness  = True,
                engine         = 'algo',
                kind           = 'bundle_build',
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, [None])
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            bin_glob = '{glob:b:\w+}'
            self._wrapped_output(
                role           = 'Binary',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                kind           = '[glob:b]',
                local          = binaries_syntax_in_workdir.replace('{}', bin_glob),
                nativefmt      = self.conf.executables_fmt,
            )
            #-------------------------------------------------------------------------------
            bin_run_glob = '{glob:b:\w+}-{glob:r:\w+}'  # OOPS : copied locally as binary-run
            self._wrapped_output(
                role           = 'Binary',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                kind           = '[glob:b]',
                local          = binaries_syntax_in_workdir.replace('{}', bin_run_glob),
                nativefmt      = self.conf.executables_fmt,
                run            = '[glob:r]',
            )
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            #pass
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

