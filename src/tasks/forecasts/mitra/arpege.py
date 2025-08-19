# -*- coding: utf-8 -*-

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
import davai

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai.vtx.hooks.namelists import hook_gnam


class Forecast(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    @property
    def experts(self):
        """Redefinition as property because of runtime/conf-determined values."""
        return [FPDict({'kind':'norms', 'hide_equal_norms':self.conf.hide_equal_norms}),
                FPDict({'kind':'fields_in_file'})
                ] + davai.vtx.util.default_experts()

    def process(self):
        self._wrapped_init()
        self._notify_start_inputs()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_listing())
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())
            self._wrapped_input(**self._reference_continuity_listing())
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Reference',  # ModelState (continuity)
                block          = self.output_block(),
                experiment     = self.conf.ref_xpid,
                fatal          = False,
                format         = '[nativefmt]',
                kind           = 'historic',
                local          = 'ref.ICMSHARPE+[term:fmthm]',
                nativefmt      = 'fa',
                term           = self.conf.expertise_term,
                vconf          = self.conf.ref_vconf,
            )
            #-------------------------------------------------------------------------------
        if 'fetch' in self.steps:
            # this task is also to be compared to another task of the same experiment
            self._wrapped_input(**self._reference_consistency_expertise())
            self._wrapped_input(**self._reference_consistency_listing())

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._load_usual_tools()  # LFI tools, ecCodes defs, ...
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RrtmConst',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'rrtm',
                local          = 'rrtm.const.tgz',
            )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            tbport = self._wrapped_input(
                role           = 'PortabilityNamelist',
                kind           = 'namelist',
                local          = 'portability.nam',
                path           = f'namelist/davai/portability/{self.conf.target_host}.nam',
                ref            = self.conf.gitenv_ref,
                repo           = self.conf.gitenv_repo,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                hook_options   = (update_namelist, tbport),
                hook_conf      = (hook_gnam, self.conf.get('nam_hook', {})),
                #hook_z         = (hook_gnam, {'NAMBLOCK':{'LKEY':True, RVALUE:0.}}),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                path           = f'namelist/mitra/global/{self._configtag.upper()}.nam',
                ref            = self.conf.gitenv_ref,
                repo           = self.conf.gitenv_repo,
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            tbx = self.flow_executable(kind='mfmodel')
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Atmospheric Initial Conditions',
                block          = self.conf.ic_block,
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                format         = '[nativefmt]',
                kind           = 'initial_condition',
                local          = 'ICMSHARPEINIT',
                nativefmt      = 'fa',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        self._notify_inputs_done()
        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                crash_witness  = True,
                drhookprof     = self.conf.drhook_profiling,
                engine         = 'parallel',
                kind           = 'forecast',
                #fcterm         = self.conf.fcst_term,
                #fcunit         = 'h',
                #timestep       = self.conf.timestep,
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'ModelState',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = '[nativefmt]',
                kind           = 'historic',
                local          = 'ICMSHARPE+{glob:term:\d+(?::\d+)?}',
                namespace      = self.REF_OUTPUT,
                nativefmt      = 'fa',
                term           = '[glob:term]',
                fatal          = False
            )
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_listing())
            self._wrapped_output(**self._output_stdeo())
            self._wrapped_output(**self._output_drhook_profiles())
            #-------------------------------------------------------------------------------

