# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
import davai

from common.util.hooks import arpifs_obs_error_correl_legacy2oops

from davai.taskutil.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai.taskutil.hooks import hook_fix_model, hook_gnam, hook_disable_fullpos, hook_disable_flowdependentb, hook_ensemble_build


class EnVarAdjoint(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'oops:op_obs_file/test_adjoint'})] + davai.vtx.util.default_experts()

    def output_block(self):
        return '-'.join([self.conf.jobname,
                         self.conf.model,
                         self.tag])

    def input_block(self):
        return '-'.join([self.conf.jobname,
                         self.conf.model,
                         'BmatSp'.lower()])

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
                role           = 'SunMoonFiles',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'sunmoonpositioncoeffs',
                local          = 'sun_moon_position.tgz',
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
                role='Coefmodel',
                format='unknown',
                genv=self.conf.appenv,
                kind='coefmodel',
                local='COEF_MODEL.BIN',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role='Stabal',
                format='unknown',
                genv=self.conf.appenv,
                kind='stabal',
                level='96',
                local='stabal[level].[stat]',
                stat='bal,cv',
            )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role='Config',
                format='json',
                genv=self.conf.appenv,
                hook_nam=(hook_ensemble_build, self.conf.members),
                intent='inout',
                kind='config',
                local='oops.[format]',
                nativefmt='[format]',
                objects='test_envar',
                scope='oops',
            )

            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role='OOPSObjectsNamelists',
                binary=self.conf.model,
                format='ascii',
                genv=self.conf.appenv,
                kind='namelist',
                local='naml_[object]',
                object=['geometry'],
                source='objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            # Fix TSTEP,CSTOP in Model objects
            # Disable FullPos use everywhere
            self._wrapped_input(
                role='OOPSModelObjectsNamelists',
                binary=self.conf.model,
                format='ascii',
                genv=self.conf.appenv,
                hook_model=(hook_fix_model, '4dvar', False),
                hook_nofullpos=(hook_disable_fullpos,),
                intent='inout',
                kind='namelist',
                local='model.nam',
                object=['nonlinear_model_upd2'],
                source='objects/[object].nam',
            )
            #-------------------------------------------------------------------------------
            # BMatrix without flow-dependent sigma_b and correlations
            self._wrapped_input(
                role='OOPSBmatrixNamelist',
                binary=self.conf.model,
                format='ascii',
                genv=self.conf.appenv,
                hook_simpleb=(hook_disable_flowdependentb,),
                intent='inout',
                kind='namelist',
                local='[object].nam',
                object=['bmatrix'],
                source='objects/[object].nam',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role='NamelistLeftovers',
                binary=self.conf.model,
                format='ascii',
                genv=self.conf.appenv,
                hook_nofullpos=(hook_disable_fullpos,),
                hook_simpleb=(hook_disable_flowdependentb,),
                hook_nstrin=(hook_gnam, {'NAMPAR1':{'NSTRIN':4}}),
                hook_cvaraux=(hook_gnam, {'NAMVAR':{'LVARBC':False, 'LTOVSCV':False}}),
                intent='inout',
                kind='namelist',
                local='fort.4',
                source='objects/leftovers_assim.nam',
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

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            # TODO: Fix error_covariance_3d_mod.F90, then remove this unused resource
            self._wrapped_input(
                role='BackgroundStdError',
                block='sigmab',
                date='{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment=self.conf.input_shelf,
                format='grib',
                kind='bgstderr',
                local='errgrib_[geometry:truncation]',
                stage='vor',
                term='3',  # FIXME: self.guess_term(force_window_start=True),
                vapp=self.conf.shelves_vapp,
                vconf=self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role='Guess',
                block='forecast',
                date='{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment=self.conf.input_shelf,
                format='fa',
                kind='historic',
                local='ICMSHOOPSINIT',
                term='6',
                vapp=self.conf.shelves_vapp,
                vconf=self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            self._wrapped_input(
                role='ModelState',
                block=self.input_block(),
                experiment=self.conf.xpid,
                format='fa',
                kind='historic',
                local= 'ICMSHM[member]_term[term:fmth]',
                member= [1,2,3,4,5,6,7,8],
                term='-3',
            )

        self._notify_inputs_done()
        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                crash_witness=True,
                drhookprof=self.conf.drhook_profiling,
                engine='parallel',
                iomethod='4',
                kind='ootest',
                terms=[-3, ],
                members=range(1, int(self.conf.members) + 1),
                test_type='b/test_adjoint',
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

