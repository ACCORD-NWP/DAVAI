# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver
from common.util.hooks import update_namelist
import davai

from davai.taskutil.mixins import DavaiIALTaskMixin, IncludesTaskMixin


class PGD(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'fields_in_file'})]
    _taskinfo_kind = 'statictaskinfo'

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
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'CoverParams',
                format         = 'foo',
                genv           = self.conf.appenv_clim,
                kind           = 'coverparams',
                local          = 'ecoclimap_covers_param.tgz',
                source         = 'ecoclimap',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Sand DB',
                format         = 'dir/hdr',
                genv           = self.conf.appenv_clim,
                kind           = 'sand',
                local          = 'sand_DB.tgz',
                source         = self.conf.sand_source,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Clay DB',
                format         = 'dir/hdr',
                genv           = self.conf.appenv_clim,
                kind           = 'clay',
                local          = 'clay_DB.tgz',
                source         = self.conf.clay_source,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Surface Type DB',
                format         = 'dir/hdr',
                genv           = self.conf.appenv_clim,
                kind           = 'surface_type',
                local          = 'surfacetype_DB.tgz',
                source         = self.conf.surface_type_source,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Orography DB',
                format         = 'dir/hdr',
                genv           = self.conf.appenv_clim,
                geometry       = self.conf.orography_geometry,
                kind           = 'orography',
                local          = 'orography_DB.tgz',
                source         = self.conf.orography_source,
            )
            #-------------------------------------------------------------------------------
            if 'bathymetry_source' in self.conf:
                self._wrapped_input(
                    role           = 'Bathymetry DB',
                    format         = 'dir/hdr',
                    genv           = self.conf.appenv_clim,
                    geometry       = self.conf.bathymetry_geometry,
                    kind           = 'bathymetry',
                    local          = 'etopo.tgz',
                    source         = self.conf.bathymetry_source,
                )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            tbgeo = self._wrapped_input(  # this is stored in shelf rather than uenv because generated by domain_maker
                role           = 'GeometryNamelist',
                binary         = 'arpege',
                block          = 'geometry',
                experiment     = self.conf.input_shelf,
                format         = 'ascii',
                geometry       = self.conf.geometry.tag,
                intent         = 'in',
                kind           = 'geoblocks',
                local          = 'geometry_blocks.nam',
                target         = 'buildpgd',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                binary         = 'arpege',
                format         = 'ascii',
                genv           = self.conf.appenv_clim,
                hook_geo       = (update_namelist, tbgeo),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'OPTIONS.nam',
                source         = '{}/namel_buildpgd'.format(self.conf.model),
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            tbx = self.flow_executable(
                kind           = 'buildpgd',
                local          = 'PGD.X',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
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
                engine         = 'blind',
                kind           = 'buildpgd',
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
                role           = 'PgdFile',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'fa',
                kind           = 'pgdfa',
                local          = 'PGD.[format]',
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

