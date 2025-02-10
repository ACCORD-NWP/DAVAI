# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
import davai

from common.util.hooks import arpifs_obs_error_correl_legacy2oops

from davai_taskutil.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai_taskutil.hooks import hook_fix_model, hook_gnam, hook_disable_fullpos, hook_disable_flowdependentb, hook_fix_varbc



class H(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    
    def output_block(self):
        return '-'.join([self.conf.model,
                         self.ND,
                         self.tag])

    def obs_input_block(self):
        return '-'.join([self.conf.model,
                         self.ND,
                         'hdirect' + self._tag_suffix()])

    def process(self):
        self._wrapped_init()
        self._notify_start_inputs()
                
        self._testid = self.conf.test_family + '/'+ self.tag.split(".")[0].split("+")[0]
        self._withvarbc = False
        self._suffix_vbc = ''
        if len(self.tag.split("+")) > 1:
            self._withvarbc = True            
            self._suffix_vbc = '_varbc'
            
        self.experts = [FPDict({'kind':'oops:'+self._testid}),FPDict({'kind':'joTables'})] + davai.util.default_experts()

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
                role           = 'SunMoonFiles',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'sunmoonpositioncoeffs',
                local          = 'sun_moon_position.tgz',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'IREmisAtlas',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'atlas_emissivity',
                local          = 'uw_ir_emis_atlas_hdf5.tar',
                source         = 'uwir',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RCorrelations(MF)',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'correlations',
                local          = 'rmtberr_[instrument].dat',
                intent         = 'inout',
                instrument     = 'iasi,cris',
                hook_convert   = (arpifs_obs_error_correl_legacy2oops,),
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AtlasEmissivity',
                format         = 'unknown',
                genv           = self.conf.appenv,
                instrument     = '[targetname]',
                kind           = 'atlas_emissivity',
                local          = 'ATLAS_[targetname:upper].BIN',
                month          = self.conf.rundate.ymdh,
                targetname     = 'ssmis,iasi,an1,an2',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AmvError',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'amv_error',
                local          = 'amv_p_and_tracking_error',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AmvBias',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'amv_bias',
                local          = 'amv_bias_info',
            )
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
                role           = 'RsBiasTables',
                format         = 'odb',
                genv           = self.conf.appenv,
                kind           = 'odbraw',
                layout         = 'RSTBIAS,COUNTRYRSTRHBIAS,SONDETYPERSTRHBIAS',
                local          = '[layout:upper]',
            )            
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Coefmodel',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'coefmodel',
                local          = 'COEF_MODEL.BIN',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ScatCmod5',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'cmod5',
                local          = 'fort.36',
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
                role           = 'Stabal',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'stabal',
                level          = '96',
                local          = 'stabal[level].[stat]',
                stat           = 'bal,cv',
            )            
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'IoassignScripts',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'ioassign_script',
                language       = 'ksh',
                local          = '[purpose]_ioassign',
                purpose        = 'create,merge',
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
                objects        = 'h_'+self.ND+self._suffix_vbc,
                scope          = 'oops',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ChannelsNamelist',
                binary         = self.conf.model,
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
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = ['geometry'],
                source         = 'objects/naml_[object]',
            )            
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'OOPSGomNamelist',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'namelist_[object]',
                object         = ['gom_setup_0', 'gom_setup', 'gom_setup_hres'],
                source         = 'objects/namelist_[object]',
            )
            #-------------------------------------------------------------------------------
            # Fix TSTEP,CSTOP in Model objects
            # Disable FullPos use everywhere
            self._wrapped_input(
                role           = 'OOPSModelObjectsNamelists',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_model     = (hook_fix_model,self.NDVar,False),
                hook_nofullpos = (hook_disable_fullpos,),                                
                intent         = 'inout',
                kind           = 'namelist',
                local          = '[object].nam',
                object         = ['observations', 'nonlinear_model_upd2','linear_model_upd2','traj_model_upd2'],
                source         = 'objects/[object].nam',
            )            
            #-------------------------------------------------------------------------------
            # BMatrix without flow-dependent sigma_b and correlations
            self._wrapped_input(
                role           = 'OOPSBmatrixNamelist',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_simpleb   = (hook_disable_flowdependentb,),                                
                intent         = 'inout', 
                kind           = 'namelist',
                local          = '[object].nam',
                object         = ['bmatrix'],
                source         = 'objects/[object].nam',
            )                        
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'NamelistLeftovers',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_nofullpos = (hook_disable_fullpos,),
                hook_simpleb   = (hook_disable_flowdependentb,),
                hook_varbc     = (hook_fix_varbc, self._withvarbc, ),                
                hook_nstrin    = (hook_gnam, {'NAMPAR1':{'NSTRIN':'NBPROC'}}),
                hook_cvaraux   = (hook_gnam, {'NAMVAR':{'NUPTRA':0}, 'NAMARG':{'NCONF':2}}),                
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'objects/leftovers_assim.nam',
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbx = self.flow_executable(
                kind='oopsbinary',
                run='ootestcomponent',
                local='OOTESTVAR.X',
            )
            #-------------------------------------------------------------------------------
            tbio = self.flow_executable(
                kind           = 'odbioassign',
                local          = 'ioassign.x',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:      
            # TODO: Fix error_covariance_3d_mod.F90, then remove this unused resource
            self._wrapped_input(
                role           = 'BackgroundStdError',
                block          = 'sigmab',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'grib',
                kind           = 'bgstderr',
                local          = 'errgrib.[variable]',
                stage          = 'vor',
                term           = '3',  # FIXME: self.guess_term(force_window_start=True),
                variable       = ['vo','ucdv','lnsp','t','q'],
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
                kind           = 'historic',
                local          = 'ICMSHOOPSINIT',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'VarBC',
                block          = '4dupd2',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
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
                local          = 'CCMA',
                layout         = 'ccma',                
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
                crash_witness   = True,
                drhookprof      = self.conf.drhook_profiling,
                engine          = 'parallel',
                ioassign        = tbio[0].container.localpath(),                
                iomethod        = '4',
                kind            = 'ootestobs',
                test_type       = self._testid,
                npool           = self.conf.obs_npools,
                slots           = self.obs_tslots,
            )
            
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.run_expertise()
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

