# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver
from common.util.hooks import update_namelist
import davai

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin


class FinalizePGD(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'fields_in_file'})]
    _taskinfo_kind = 'statictaskinfo'

    def _flow_input_pgd_block(self):
        return '-'.join([self.conf.prefix,
                         'pgd',
                         self.conf.model,
                         self.conf.geometry.tag])

    def _flow_input_clim_block(self):
        return '-'.join([self.conf.prefix,
                         'c923',
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
            self._wrapped_input(
                role           = 'Reference',  # PgdFile
                block          = self.output_block(),
                experiment     = self.conf.ref_xpid,
                fatal          = False,
                format         = 'fa',
                kind           = 'pgdfa',
                local          = 'ref.PGD.[format]',
                vconf          = self.conf.ref_vconf,
            )
            #-------------------------------------------------------------------------------

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._load_usual_tools()  # LFI tools, ecCodes defs, ...
            pass
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            pass
            
        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            pass

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:

            # PGD file
            self._wrapped_input(
                role           = 'InputPGD',
                #block         = 'geo-pgd-arome-{}'.format(self.conf.geometry.tag),
                block          = self._flow_input_pgd_block(),
                experiment     = self.conf.xpid,
                intent         = 'inout',
                format         = 'fa',
                kind           = 'pgdfa',
                local          = 'PGD.[format]',
                nativefmt      = 'fa',
            )

            
            # CLIM file with spectrally fitted orography
            self._wrapped_input(
                role           = 'Clim',
                block          = self._flow_input_clim_block(),
                experiment     = self.conf.xpid,
                format         = 'fa',
                kind           = 'clim_model',
                local          = 'Const.Clim',
            )
            

        self._notify_inputs_done()
        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
              engine         = 'algo',
              kind           = 'set_filtered_orog_in_pgd',
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, [None])
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_output(
              role           = 'FinalPgd',
              block          = self.output_block(),
              experiment     = self.conf.xpid,
              format         = 'fa',
              kind           = 'pgdfa',
              local          = 'PGD.[format]',
              namespace      = self.REF_OUTPUT,
              nativefmt      = 'fa',
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

