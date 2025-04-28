# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver
from common.util.hooks import update_namelist
import davai

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin


class Prep(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'fields_in_file'})]

    def _flow_input_pgd_block(self):
        return '-'.join([self.conf.prefix,
                         'finalize-pgd' if self.conf.get('filtered_orography_in_pgd') else 'pgd',
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
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Reference',  # Surface output IC
                block          = self.output_block(),
                experiment     = self.conf.ref_xpid,
                filling        = 'surf',
                fatal          = False,
                format         = 'fa',
                kind           = 'ic',
                local          = 'ref.PREP1_interpolated.[format]',
                model          = 'surfex',
                vconf          = self.conf.ref_vconf,
            )
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
                role           = 'Initial Clim',  # PGD
                format         = 'fa',
                genv           = self.conf.davaienv,
                geometry       = self.conf.prep_initial_geometry,
                kind           = 'pgdfa',
                local          = 'PGD1.[format]',
                gvar           = 'pgd_fa_[geometry::tag]',
            )
            #-------------------------------------------------------------------------------
            if self.conf.pgd_source == 'static':
                # else: 2.1
                self._wrapped_input(
                    role           = 'Target Clim',  # PGD
                    format         = 'fa',
                    genv           = self.conf.davaienv,
                    geometry       = self.conf.geometry,
                    kind           = 'pgdfa',
                    local          = 'PGD.[format]',
                    gvar           = 'pgd_fa_[geometry::tag]',
                )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Namelist',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.davaienv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'OPTIONS.nam',
                source         = 'SFX/{}/namel_prep'.format(self.conf.model),
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            tbx = self.flow_executable(
                kind           = 'prep',
                local          = 'PREP.X',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Surface Initial Conditions',
                block          = 'forecast',
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                geometry       = self.conf.prep_initial_geometry,
                kind           = 'historic',
                local          = 'PREP1.[format]',
                model          = 'surfex',
                origin         = 'forecast',
                term           = 0,
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            if self.conf.pgd_source == 'flow':
                # else: 1.1.1
                self._wrapped_input(
                    role           = 'Target Clim',  # PGD
                    block          = self._flow_input_pgd_block(),
                    experiment     = self.conf.xpid,
                    format         = 'fa',
                    geometry       = self.conf.geometry,
                    kind           = 'pgdfa',
                    local          = 'PGD.[format]',
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
                engine         = 'blind',
                kind           = 'prep',
                underlyingformat = 'fa',
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
                role           = 'Target Surface Conditions',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                filling        = 'surf',
                format         = 'fa',
                kind           = 'ic',
                local          = 'PREP1_interpolated.[format]',
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
            #-------------------------------------------------------------------------------
