# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict, FPSet

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist

from davai.vtx.tasks.mixins import DavaiTaskMixin


class BatorODB(Task, DavaiTaskMixin):

    experts = [FPDict({'kind':'bator_obscount'}), FPDict({'kind':'bator_profile'})]

    def output_block(self):
        return '-'.join([self.conf.model,
                         self.conf.assim_scheme,
                         self.tag])

    def process(self):
        self._wrapped_init()
        self._obstype_rundate_association()
        self._notify_start_inputs()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'AvgMasks',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'avgmask',
                local          = 'mask.[sensor]',
                sensor         = 'atms,ssmis,mwts2',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BatodbConfigurationFile',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'batodbconf',
                local          = 'param.cfg',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'CreateIoassignScript',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'ioassign_script',
                language       = 'ksh',
                local          = '[purpose]_ioassign',
                purpose        = 'create',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'GPSList',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'gpslist',
                local          = 'list_gpssol',
            )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbnamreduc = self._wrapped_input(
                role           = 'BatodbReductionDelta',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.davaienv,
                kind           = 'namelist',
                local          = 'delta-bator_reduction.[model].davai.nam',
                source         = 'davai/[local]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'NamelistBatodb',
                binary         = 'batodb',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_obs_reduc = (update_namelist, tbnamreduc),
                intent         = 'inout',
                kind           = 'namutil',
                local          = 'NAMELIST',
                source         = self.conf.bator_namelist,
            )
            #-------------------------------------------------------------------------------
            if self.conf.LAM:
                self._wrapped_input(
                    role           = 'NamelistLamflag',
                    #binary         = self.conf.model,
                    binary         = 'arpifs',
                    format         = 'ascii',
                    genv           = self.conf.davaienv,
                    kind           = 'namelist',
                    local          = 'NAM_lamflag',
                    #source         = 'namel_lamflag_odb',
                    source         = 'geometries/france10km.lamflag_odb.nam',
                )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbio = self.flow_executable(
                kind           = 'odbioassign',
                local          = 'ioassign',
            )
            #-------------------------------------------------------------------------------
            tbx = self.flow_executable(
                kind           = 'batodb',
                local          = 'BATODB.X',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            obstype = self.conf.get('obstype', None)
            tbmap = self._wrapped_input(
                role           = 'Obsmap',
                block          = 'obsraw',
                experiment     = self.conf.input_shelf,
                format         = 'ascii',
                kind           = 'obsmap',
                local          = 'batodb_map',
                # if obstype is not specified (in conf or loop), get all obstypes from Bator Map:
                only           = FPSet([obstype]) if obstype else None,
                discard        = FPSet([self.conf.discard_obstype]) if 'discard_obstype' in self.conf else None,
                scope          = self.conf.obsmap_scope,
                stage          = 'extract',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Observations',
                block          = 'obsraw',
                experiment     = self.conf.input_shelf,
                fatal          = False,
                format         = '[helper:getfmt]',
                helper         = tbmap[0].contents,
                kind           = 'observations',
                local          = '[actualfmt].[part]',
                part           = tbmap[0].contents.dataset(),
                stage          = 'extract',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BlacklistGlobal',
                block          = 'obsraw',
                experiment     = self.conf.input_shelf,
                format         = 'ascii',
                kind           = 'blacklist',
                local          = 'LISTE_NOIRE_DIAP',
                scope          = 'global',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BlacklistLocal',
                block          = 'obsraw',
                experiment     = self.conf.input_shelf,
                format         = 'ascii',
                kind           = 'blacklist',
                local          = 'LISTE_LOC',
                scope          = 'local',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass

        self._notify_inputs_done()
        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                drhookprof     = self.conf.drhook_profiling,
                engine         = 'parallel',
                ioassign       = tbio[0].container.localpath(),
                iomethod       = '4',
                kind           = 'raw2odb',
                lamflag        = self.conf.LAM,
                npool          = self.conf.obs_npools,
                ntasks         = self.conf.ntasks,
                parallel_const = self.conf.obs_paraconst,
                slots          = self.obs_tslots,
                taskset        = 'socketpacked',
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            tbmapout = self._wrapped_output(
                role           = 'ObsmapUsed',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'ascii',
                kind           = 'obsmap',
                local          = 'batodb_map.out',
                stage          = 'build',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'ObservationsODB',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                kind           = 'observations',
                local          = 'ECMA.[part]',
                part           = tbmapout[0].contents.odbset(),
                stage          = 'build',
            )
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(
                role           = 'Listing',
                binary         = 'batodb',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'ascii',
                kind           = 'listing',
                local          = 'listing.[part]',
                namespace      = self.REF_OUTPUT,
                part           = tbmapout[0].contents.odbset(),
                task           = self._configtag,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'ParallelExecSynthesis',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'json',
                kind           = 'taskinfo',
                local          = 'parallel_exec_synthesis.[format]',
                nativefmt      = '[format]',
                scope          = 'parallelprofiling',
                task           = self._configtag,
            )
            #-------------------------------------------------------------------------------

