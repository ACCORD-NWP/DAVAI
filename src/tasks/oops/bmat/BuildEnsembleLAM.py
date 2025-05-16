# -*- coding: utf-8 -*-

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
import davai

from common.util.hooks import arpifs_obs_error_correl_legacy2oops

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai.vtx.hooks.namelists import hook_fix_model, hook_gnam, hook_disable_fullpos, hook_disable_flowdependentb, hook_ensemble_build


class BuildEnsemble(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'fields_in_file'})] + davai.vtx.util.default_experts()

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
                role           = 'RrtmConst',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'rrtm',
                local          = 'rrtm.const.tgz',
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
                hook_nam       = (hook_ensemble_build, self.conf.members),  # generate namelist to write member
                intent         = 'inout',
                kind           = 'config',
                local          = 'oops.[format]',
                nativefmt      = '[format]',
                objects        = 'build_ensemble_aro',
                scope          = 'oops',
            )

            #-------------------------------------------------------------------------------
            # Geometry
            self._wrapped_input(
                role           = 'OOPSObjectsNamelists',
                binary         = self.conf.model,
                format         = 'ascii',
                intent         = 'inout',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = ['standard_geometry'],
                source         = 'objects/naml_[object]',
            )
            # BMatrix without flow-dependent sigma_b and correlations
            self._wrapped_input(
                role           = 'OOPSObjectsNamelists',
                binary         = self.conf.model,
                format         = 'ascii',
                intent         = 'inout',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = ['bmatrix_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            # Set TSTEP in Model objects
            self._wrapped_input(
                role           = 'OOPSModelObjectsNamelists',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'naml_[object]',
                hook_tstep     = (hook_gnam, {'NAMRIP':{'TSTEP':1800.}}),
                object         = ['nonlinear_model_3dv_aro', 'linear_model_aro', 'traj_model_3dv_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'NamelistLeftovers',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                hook_cvaraux   = (hook_gnam, {'NAMVAR':{'LVARBC':False, 'LTOVSCV':False}}),
                hook_nstrin    = (hook_gnam, {'NAMPAR1':{'NSTRIN':'NBPROC'}}),
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'objects/naml_leftovers_aro',
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

        self._notify_inputs_done()
        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                crash_witness  = True,
                drhookprof     = self.conf.drhook_profiling,
                engine         = 'parallel',
                iomethod       = '4',
                kind           = 'ootest',
                terms          = [-3, ],
                members        = range(1, int(self.conf.members) + 1),
                test_type      = 'ensemble/build',
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
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHM[member]+0000',
                term           = '-3',
                member         = [1,2,3,4,5,6,7,8],
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

