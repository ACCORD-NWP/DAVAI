# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver
from common.util.hooks import update_namelist
import davai

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai.vtx.hooks.namelists import hook_gnam


class StandaloneArpegeForecast(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    @property
    def experts(self):
        """Redefinition as property because of runtime/conf-determined values."""
        return [FPDict({'kind':'norms', 'plot_spectral':True, 'hide_equal_norms':self.conf.hide_equal_norms}),
                FPDict({'kind':'fields_in_file'})
                ] + davai.vtx.util.default_experts()

    def _flow_input_pgd_block(self):
        """Block of PGD in case of a PPF flow-chained job."""
        return '-'.join([self.conf.prefix,
                         'pgd',
                         self.conf.model,
                         self.conf.geometry.tag])

    def _flow_input_surf_ic_block(self):
        """Block of surf IC in case of a PPF flow-chained job."""
        return '-'.join([self.conf.prefix,
                         'prep',
                         self.conf.model,
                         self.conf.geometry.tag])

    def output_block(self):
        return '-'.join([self.conf.prefix,
                         self.tag])

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
                role           = 'Reference',  # ModelState
                block          = self.output_block(),
                experiment     = self.conf.ref_xpid,
                fatal          = False,
                format         = '[nativefmt]',
                kind           = 'historic',
                local          = 'ref.ICMSHFCST+[term:fmthm]',
                nativefmt      = 'fa',
                term           = self.conf.expertise_term,
                vconf          = self.conf.ref_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Reference',  # SurfState
                block          = self.output_block(),
                experiment     = self.conf.ref_xpid,
                fatal          = False,
                format         = '[nativefmt]',
                kind           = 'historic',
                local          = 'ref.ICMSHFCST+[term:fmthm].sfx',
                model          = 'surfex',
                nativefmt      = 'fa',
                term           = self.conf.expertise_term,
                vconf          = self.conf.ref_vconf,
            )
            #-------------------------------------------------------------------------------

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._load_usual_tools()  # LFI tools, ecCodes defs, ...
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RrtmConst',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'rrtm',
                local          = 'rrtm.const.tgz',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RtCoef',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'rtcoef',
                local          = 'var.sat.misc_rtcoef.01.tgz',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'CoverParams',
                format         = 'foo',
                genv           = self.conf.appenv,
                kind           = 'coverparams',
                local          = 'ecoclimap_covers_param.tgz',
                source         = 'ecoclimap',
            )
            #-------------------------------------------------------------------------------
            if self.conf.pgd_source == 'static':
                self._wrapped_input(
                    role           = 'ClimPGD',
                    format         = 'fa',
                    genv           = self.conf.davaienv,
                    gvar           = 'pgd_fa_[geometry::tag]',
                    kind           = 'pgdfa',
                    local          = 'Const.Clim.sfx',
                )
                # else: 2.1
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Global Clim',
                format         = 'fa',
                genv           = self.conf.davaienv,
                kind           = 'clim_model',
                local          = 'Const.Clim',
                month          = self.conf.rundate,
            )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'NamelistSurfex',
                binary         = '[model]',
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'EXSEG1.nam',
                source         = 'namel_previ_surfex',
            )
            #-------------------------------------------------------------------------------
            # deactivate FPinline & DDH, activate spnorms:
            tboptions = self._wrapped_input(
                role           = 'Namelist Deltas to add/remove options',
                binary         = 'arpifs',
                component      = self.conf.namelist_components,
                format         = 'ascii',
                genv           = self.conf.davaienv,
                intent         = 'in',
                kind           = 'namelist',
                local          = '[component]',
                source         = 'model/options_delta/[component]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                binary         = '[model]',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_options   = (update_namelist, tboptions),
                #hook_z         = (hook_gnam, {'NAMBLOCK':{'LKEY':True, RVALUE:0.}}),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'namelistfc',
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
                block          = '4dupd2',
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                format         = '[nativefmt]',
                kind           = 'analysis',
                local          = 'ICMSHFCSTINIT',
                nativefmt      = 'fa',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            if self.conf.surf_ic_source == 'static':
                self._wrapped_input(
                    role           = 'Surface Initial conditions',
                    block          = 'surfan',
                    date           = self.conf.rundate,
                    experiment     = self.conf.input_shelf,
                    filling        = 'surf',
                    format         = '[nativefmt]',
                    kind           = 'analysis',
                    local          = 'ICMSHFCSTINIT.sfx',
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
                    block          = self._flow_input_pgd_block(),
                    experiment     = self.conf.xpid,
                    format         = 'fa',
                    kind           = 'pgdfa',
                    local          = 'Const.Clim.sfx',
                )
                # else: 1.1.1
            #-------------------------------------------------------------------------------
            if self.conf.surf_ic_source == 'flow':
                self._wrapped_input(
                    role           = 'Surface Initial conditions',
                    block          = self._flow_input_surf_ic_block(),
                    date           = self.conf.rundate,
                    experiment     = self.conf.xpid,
                    format         = '[nativefmt]',
                    filling        = 'surf',
                    kind           = 'ic',
                    local          = 'ICMSHFCSTINIT.sfx',
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
                kind           = 'forecast',
                fcterm         = self.conf.fcst_term,
                fcunit         = 'h',
                timestep       = self.conf.timestep,
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
                local          = 'ICMSHFCST+{glob:term:\d+(?::\d+)?}',
                namespace      = self.REF_OUTPUT,
                nativefmt      = 'fa',
                term           = '[glob:term]',
                fatal          = False
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'SurfState',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = '[nativefmt]',
                kind           = 'historic',
                local          = 'ICMSHFCST+{glob:term:\d+(?::\d+)?}.sfx',
                model          = 'surfex',
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

