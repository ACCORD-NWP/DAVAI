# -*- coding: utf-8 -*-

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
import davai

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai.vtx.hooks.namelists import hook_gnam


class MUSCForecast(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    @property
    def experts(self):
        """Redefinition as property because of runtime/conf-determined values."""
        return [FPDict({'kind':'norms', 'hide_equal_norms':self.conf.hide_equal_norms}),
                #FPDict({'kind':'fields_in_file'}),  # FIXME: epygram not able to read them yet
                FPDict({'kind':'ddh'})
                ] + davai.vtx.util.default_experts()

    @property
    def model(self):
        """ASSUMES task tag starts with model !!!"""
        return self._configtag.split('_')[0]

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
                model          = self.model,
                nativefmt      = 'fa',
                term           = self.conf.expertise_term,
                vconf          = self.conf.ref_vconf,
            )
            #-------------------------------------------------------------------------------
            #self._wrapped_input(
            #    role           = 'Reference',  # SurfState (continuity)
            #    block          = self.output_block(),
            #    experiment     = self.conf.ref_xpid,
            #    fatal          = False,
            #    kind           = 'historic',
            #    local          = 'ref.ICMSHFCST+[term:fmthm].sfx',
            #    model          = 'surfex',
            #    nativefmt      = 'fa',
            #    term           = self.conf.expertise_term,
            #    vconf          = self.conf.ref_vconf,
            #)
            ##-------------------------------------------------------------------------------
            # These are not exactly DDH but considered as such for the sake of the DDH expert comparison
            self._wrapped_input(
                role           = 'Reference',  # MUSC special output
                block          = self.output_block(),
                experiment     = self.conf.ref_xpid,
                fatal          = False,
                kind           = 'ddh',
                local          = 'ref.Out.[term:fmth].0000.lfa',  # 0000: we save (and compare) only round hours
                model          = self.model,
                nativefmt      = 'lfa',
                scope          = 'dlimited',
                term           = self.conf.expertise_term,
                vconf          = self.conf.ref_vconf,
            )

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
            self._wrapped_input(
                role           = 'CoverParams',
                format         = 'foo',
                genv           = self.conf.commonenv,
                kind           = 'coverparams',
                local          = 'ecoclimap_covers_param.tgz',
                source         = 'ecoclimap',
            )
            #-------------------------------------------------------------------------------
            if self.conf.pgd_source == 'static':
                self._wrapped_input(
                    role           = 'ClimPGD',
                    nativefmt      = 'fa',
                    genv           = self.conf.davaienv,
                    gvar           = 'pgd_fa_[geometry::tag]',
                    kind           = 'pgdfa',
                    local          = 'Const.Clim.sfx',
                )
            # else: 2.1
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'NamelistSurfex',
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'EXSEG1.nam',
                path           = f'namelist/{self.conf.suite_vapp}/{self.conf.suite_vconf}/surfex.nam',
                ref            = self.conf.gitenv_ref,
                repo           = self.conf.gitenv_repo,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                hook_conf      = (hook_gnam, self.conf.get('nam_hook', {})),
                #hook_z         = (hook_gnam, {'NAMBLOCK':{'LKEY':True, RVALUE:0.}}),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                path           = f'namelist/{self.conf.suite_vapp}/{self.conf.suite_vconf}/{self._configtag}.nam',
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
                block          = 'init',
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                kind           = 'initial_condition',
                local          = 'ICMSHARPEINIT',
                model          = self.model,
                nativefmt      = 'fa',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            if self.conf.surf_ic_source == 'static':
                self._wrapped_input(
                    role           = 'Surface Initial conditions',
                    block          = 'init',
                    date           = self.conf.rundate,
                    experiment     = self.conf.input_shelf,
                    filling        = 'surf',
                    kind           = 'initial_condition',
                    local          = 'ICMSHARPEINIT.sfx',
                    model          = 'surfex',
                    nativefmt      = 'fa',
                    vapp           = self.conf.shelves_vapp,
                    vconf          = self.conf.shelves_vconf,
                )
                # else: 2.1
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            if self.conf.pgd_source == 'flow':
                self._wrapped_input(
                    role           = 'PGD',
                    block          = self.input_block('pgd'),
                    experiment     = self.conf.xpid,
                    nativefmt      = 'fa',
                    kind           = 'pgdfa',
                    local          = 'Const.Clim.sfx',
                    model          = self.model,
                )
                # else: 1.1.1
            #-------------------------------------------------------------------------------
            if self.conf.surf_ic_source == 'flow':
                self._wrapped_input(
                    role           = 'Surface Initial conditions',
                    block          = self.input_block('prep'),
                    date           = self.conf.rundate,
                    experiment     = self.conf.xpid,
                    filling        = 'surf',
                    kind           = 'ic',
                    local          = 'ICMSHARPEINIT.sfx',
                    model          = 'surfex',
                    nativefmt      = 'fa',
                )
                # else: 1.2
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
                kind           = 'musc',
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
                model          = self.model,
                namespace      = self.REF_OUTPUT,
                nativefmt      = 'fa',
                term           = '[glob:term]',
                fatal          = False
            )
            #-------------------------------------------------------------------------------
            #self._wrapped_output(
            #    role           = 'SurfState',
            #    block          = self.output_block(),
            #    experiment     = self.conf.xpid,
            #    format         = '[nativefmt]',
            #    kind           = 'historic',
            #    local          = 'ICMSHFCST+{glob:term:\d+(?::\d+)?}.sfx',
            #    model          = 'surfex',
            #    namespace      = self.REF_OUTPUT,
            #    nativefmt      = 'fa',
            #    term           = '[glob:term]',
            #    fatal          = False
            #)
            #-------------------------------------------------------------------------------
            # These are not exactly DDH but considered as such for the sake of the DDH expert comparison
            self._wrapped_output(
                role           = 'DDHoutput',
                scope          = 'dlimited',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                kind           = 'ddh',
                local          = 'Out.{glob:term:\d+}.0000.lfa',  # 0000: we save (and compare) only round hours
                model          = self.model,
                namespace      = self.REF_OUTPUT,
                nativefmt      = 'lfa',
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

