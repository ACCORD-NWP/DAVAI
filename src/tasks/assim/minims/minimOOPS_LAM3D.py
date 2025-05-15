# -*- coding: utf-8 -*-

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
from common.util.hooks import arpifs_obs_error_correl_legacy2oops
import davai

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai.vtx.hooks.namelists import hook_gnam


class MinimNoVARBC(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'joTables'})] + davai.vtx.util.default_experts()
    _flow_input_task_tag = 'screening'

    def process(self):
        self._wrapped_init()
        self._obstype_rundate_association()
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
                role           = 'GetIREmisAtlasInHDF',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                source         = 'uwir',
                kind           = 'atlas_emissivity',
                local          = 'uw_ir_emis_atlas_hdf5.tar',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'MwaveRtCoef',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'mwave_rtcoef',
                local          = 'mwave_resources.tgz',
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
                role           = 'Config',
                format         = 'json',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'config',
                local          = 'oops.[format]',
                nativefmt      = '[format]',
                objects        = 'minim-3DVar_aro',
                scope          = 'oops',
            )
            #-------------------------------------------------------------------------------
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
            self._wrapped_input(
                role           = 'OOPSObjectsNamelists',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = ['standard_geometry','bmatrix_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'OOPSObsObjectsNamelists',
                format         = 'ascii',
                intent         = 'inout',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = ['observations_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'OOPSGomNamelists',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'namelist_[object]',
                object         = ['gom_setup_0', 'gom_setup_hres'],  #, 'jb_cov'
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'OOPSModelObjectsNamelists',
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'naml_[object]',
                hook_tstep     = (hook_gnam, {'NAMRIP':{'TSTEP':7200.}}),
                object         = ['nonlinear_model_3dv_aro', 'linear_model_aro', 'traj_model_3dv_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'OOPSWriteObjectsNamelists',
                format         = 'ascii',
                intent         = 'inout',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                hook_write     = (hook_gnam, {'NAMOOPSWRITE':{'CDMEXP':'MXMINI'}}),
                object         = ['write_analysis_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            tbnam_leftovers = self._wrapped_input(
                role           = 'NamelistLeftovers',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_cvaraux   = (hook_gnam, {'NAMVAR':{'LVARBC':False, 'LTOVSCV':False}}),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'objects/naml_leftovers_aro',
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbx = self.flow_executable(
                kind           = 'oopsbinary',
                run            = 'oovar',
                local          = 'OOVAR.X',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Guess',
                block          = 'cplguess',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHOOPSINIT',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Observations',
                block          = self.input_block(),
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
                kind           = 'oominim',
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
                local          = 'ICMSHMXMI+0000',
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

