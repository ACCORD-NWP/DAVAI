# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
import davai

from davai_taskutil.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai_taskutil.hooks import hook_OOPS_2_CNT0


class Minim(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'joTables'})] + davai.util.default_experts()

    def output_block(self):
        return '-'.join([self.conf.model,
                         self.NDVar,
                         self.tag])

    def obs_input_block(self):
        return '-'.join([self.conf.model,
                         self.NDVar,
                         'screening' + self._tag_suffix()])

    def process(self):
        self._wrapped_init()
        self._obstype_rundate_association()
        self._notify_start_inputs()

        # 0.0/ Promises
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
            # FIXME: not anymore in Arpege cycle / commonenv
            self._wrapped_input(
                role           = 'GetIREmisAtlasInHDF',
                format         = 'ascii',
                #genv           = self.conf.commonenv,
                genv           = self.conf.davaienv,
                instrument     = '[targetname]',
                kind           = 'atlas_emissivity',
                local          = 'uw_ir_emis_atlas_hdf5.tar',
                targetname     = 'iasi',
            )
            #-------------------------------------------------------------------------------
            # FIXME: not anymore in Arpege cycle / commonenv
            self._wrapped_input(
                role           = 'RCorrelations(MF)',
                format         = 'unknown',
                #genv           = self.conf.commonenv,
                genv           = self.conf.davaienv,
                kind           = 'correl',
                local          = '[scope]_correlation.dat',
                scope          = 'iasi,cris',
            )
            #-------------------------------------------------------------------------------
            # FIXME: not anymore in Arpege cycle / commonenv
            self._wrapped_input(
                role           = 'AtlasEmissivity',
                format         = 'unknown',
                #genv           = self.conf.commonenv,
                genv           = self.conf.davaienv,
                instrument     = '[targetname]',
                kind           = 'atlas_emissivity',
                local          = 'ATLAS_[targetname:upper].BIN',
                month          = self.conf.rundate,
                targetname     = 'ssmis,iasi,an1,an2',
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
                role           = 'RrtmConst',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'rrtm',
                local          = 'rrtm.const.tgz',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Coefmodel',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'coefmodel',
                local          = 'COEF_MODEL.BIN',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ScatCmod5',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'cmod5',
                local          = 'fort.36',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RtCoef',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'rtcoef',
                local          = 'var.sat.misc_rtcoef.01.tgz',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Stabal',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'stabal',
                level          = '41',
                local          = 'stabal96.[stat]',
                stat           = 'bal,cv',
            )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'ChannelsNamelist',
                binary         = 'arpege',
                channel        = 'cris331,iasi314',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'namchannels_[channel]',
                source         = 'namelist[channel]',
            )
            #-------------------------------------------------------------------------------
            tbnam_objects = self._wrapped_input(
                role           = 'OOPSObjectsNamelists',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.davaienv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = ['observations_tlad','standard_geometry','bmatrix'],
                source         = 'OOPS_ARO/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            tbnam_modelobjects = self._wrapped_input(
                role           = 'OOPSModelObjectsNamelists',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.davaienv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = 'nonlinear_model',
                source         = 'OOPS_ARO/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            tbnam_leftovers = self._wrapped_input(
                role           = 'NamelistLeftovers',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.davaienv,
                hook_oops2cnt0 = (hook_OOPS_2_CNT0,),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'namelist_oops',
                source         = 'OOPS_ARO/namelist_oops_leftovers',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_merge_nam = (update_namelist,
                                  tbnam_leftovers, tbnam_modelobjects, tbnam_objects),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'namel_minim',
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbx = self.flow_executable()  # default kind is masterodb, locally named '{MODEL}.X'
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Guess',
                block          = 'forecast',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHMINIINIT',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'InitialCondition',
                block          = 'forecast',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHMINIIMIN',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Background',
                block          = 'forecast',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMRFMINI0000',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'VarBC',
                block          = 'minim',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'ascii',
                intent         = 'inout',
                kind           = 'varbc',
                local          = 'VARBC.cycle',
                stage          = 'traj',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Observations',
                block          = self.obs_input_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                intent         = 'inout',
                kind           = 'observations',
                layout         = 'ccma',
                local          = 'CCMA',
                part           = 'mix',
                stage          = 'screening',
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
                kind           = 'minim',
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            self._wrapped_output(
                role           = 'Observations',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                kind           = 'observations',
                layout         = 'ccma',
                local          = '[layout:upper]',
                part           = 'mix',
                stage          = 'minim',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'Analysis',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'fa',
                kind           = 'analysis',
                local          = 'MXMINI999+0000',
                namespace      = self.REF_OUTPUT,
            )

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

