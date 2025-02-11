# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
import davai

from davai.taskutil.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai.taskutil.hooks import hook_gnam


class Canari(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    @property
    def experts(self):
        """Redefinition as property because of runtime/conf-determined values."""
        return [FPDict({'kind':'canari_stats'}),
                FPDict({'kind':'norms', 'hide_equal_norms':self.conf.hide_equal_norms})
                ] + davai.util.default_experts()

    def output_block(self):
        return '-'.join([self.conf.model,
                         self.conf.assim_scheme,
                         self.tag])

    def obs_input_block(self):
        return '-'.join([self.conf.model,
                         self.conf.assim_scheme,
                         'batodb' + self._tag_suffix()])

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

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._load_usual_tools()  # LFI tools, ecCodes defs, ...
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
            self._wrapped_input(
                role           = 'Isba Parameters',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'isbaan',
                local          = 'fort.61',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AmvError',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'amv_error',
                local          = 'amv_p_and_tracking_error',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AmvBias',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'amv_bias',
                local          = 'amv_bias_info',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ClimPGD',
                format         = 'fa',
                genv           = self.conf.davaienv,
                gvar           = 'pgd_fa_[geometry::tag]',
                kind           = 'pgdfa',
                local          = 'Const.Clim.sfx',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Current Global Clim',
                format         = 'fa',
                genv           = self.conf.davaienv,
                gvar           = 'clim_[model]_[geometry::tag]',
                kind           = 'clim_model',
                local          = 'ICMSHCANSCLIM',
                month          = self.conf.rundate,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Closest Global Clim',
                format         = 'fa',
                genv           = self.conf.davaienv,
                gvar           = 'clim_[model]_[geometry::tag]',
                kind           = 'clim_model',
                local          = 'ICMSHCANSCLI2',
                month          = self.conf.rundate.month + (1 if self.conf.rundate.day > 15 else -1),
            )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelistsurf',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_sic       = (hook_gnam, {'NAM_SEAICEn':{'LSIC_CST':True}}),  # FIXME: until update CI
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'EXSEG1.nam',
                source         = 'namel_ana_surfex',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                binary         = '[model]',
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'namel_canari',
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            tbx = self.flow_executable()
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'SurfaceGuess',
                block          = 'forecast',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                intent         = 'inout',
                kind           = 'historic',
                local          = 'ICMSHCANSINIT.sfx,ICMSHCANS+0000.sfx',
                model          = 'surfex',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            tbana = self._wrapped_input(
                role           = 'Analysis',
                block          = 'surfan',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                filling        = 'surf',
                format         = 'fa',
                kind           = 'analysis',
                local          = 'analyse.fa',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Guess',
                block          = 'forecast',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                hook_ts        = ('common.util.usepygram.overwritefield',
                                  tbana[0], ('SURFTEMPERATURE',), None, dict(KNBPDG=24)),
                intent         = 'inout',
                kind           = 'historic',
                local          = 'ICMSHCANSINIT',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'SST Analysis',
                block          = 'c931',
                experiment     = self.conf.input_shelf,
                fields         = 'sst',
                format         = 'fa',
                geometry       = self.conf.sst_geometry,
                kind           = 'geofields',
                local          = 'ICMSHCANSSST',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Sea Ice Analysis',
                block          = 'c932',
                experiment     = self.conf.input_shelf,
                fields         = 'seaice',
                format         = 'fa',
                geometry       = self.conf.seaice_geometry,
                kind           = 'geofields',
                local          = 'ICMSHCANSSEAICE',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Observations',
                block          = self.obs_input_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                intent         = 'in',
                kind           = 'observations',
                local          = 'ECMA_CAN',
                part           = 'surf',
                stage          = 'build',
            )
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
                kind           = 'canari',
                npool          = self.conf.obs_npools,
                timestep       = 1,
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
                role           = 'Surface Analysis',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                filling        = 'surf',
                format         = 'fa',
                kind           = 'analysis',
                local          = 'ICMSHCANS+0000',
                namespace      = self.REF_OUTPUT,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'Surfex Analysis',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                filling        = 'surf',
                format         = 'fa',
                kind           = 'analysis',
                local          = 'ICMSHCANS+0000.sfx',
                model          = 'surfex',
                namespace      = self.REF_OUTPUT,
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

