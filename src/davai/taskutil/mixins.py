#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mixins for Tasks, containing useful functionalities.
"""
import io
import os

from vortex import toolbox
from bronx.stdtypes.date import Period, utcnow

from ..vtx.util import context_info_for_task_summary
from ..vtx.hooks.summaries import take_the_DAVAI_train
from . import gmkpack_executables_block_tag


class IncludesTaskMixin(object):
    """Provide a method to input usual tools, known as 'Task Includes' in Olive."""

    def _load_usual_tools(self):
        if 'early-fetch' in self.steps:
            self.sh.title('Toolbox usual-tools tb_ut01')
            tb_ut01 = toolbox.input(
                role           = 'LFIScripts',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'lfiscripts',
                local          = 'usualtools/tools.lfi.tgz',
            )
            print(self.ticket.prompt, 'tb_ut01 =', tb_ut01)
            print()
            #-------------------------------------------------------------------------------
            self.sh.title('Toolbox usual-tools tb_ut02')
            tb_ut02 = toolbox.input(
                role           = 'IOPoll',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'iopoll',
                language       = 'perl',
                local          = 'usualtools/io_poll',
            )
            print(self.ticket.prompt, 'tb_ut02 =', tb_ut02)
            print()
            #-------------------------------------------------------------------------------
            self.sh.title('Toolbox usual-tools tb_ut03')
            tb_ut03 = toolbox.executable(
                role           = 'LFITOOLS',
                block          = self.executables_block(),
                experiment     = self.conf.xpid,
                kind           = 'lfitools',
                local          = 'usualtools/lfitools',
                nativefmt      = self.conf.executables_fmt,
            )
            print(self.ticket.prompt, 'tb_ut03 =', tb_ut03)
            print()
            #-------------------------------------------------------------------------------
            self.sh.title('Toolbox usual-tools tb_ut04')
            tb_ut04 = toolbox.input(
                role           = 'AdditionalGribAPIDefinitions',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'gribapiconf',
                local          = 'extra_grib_defs/gribdef.tgz',
                target         = 'definitions',
            )
            print(self.ticket.prompt, 'tb_ut04 =', tb_ut04)
            print()
        return tb_ut01, tb_ut02, tb_ut03, tb_ut04


class WrappedToolboxMixin(object):
    """
    Provide useful methods for IOs.

    Requires process() method to call _wrapped_init() to set additional attributes
    """

    REF_OUTPUT = '__archive_if_ref__'
    DEFAULT_OUTPUT_NAMESPACE = 'vortex.cache.fr'

    def output_namespace(self, namespace):
        """Return appropriate 'namespace' according to config options."""
        if namespace == self.REF_OUTPUT and self.conf.archive_as_ref:
            return 'vortex.multi.fr'
        elif namespace in ('vortex.multi.fr', 'vortex.cache.fr', 'vortex.archive.fr'):
            return namespace
        else:
            return self.DEFAULT_OUTPUT_NAMESPACE

    def _wrapped_init(self):
        """Initializations for _wrapped_*() methods."""
        self._tb_input = []
        self._tb_promise = []
        self._tb_exec = []
        self._tb_output = []

    def _wrapped_input(self, **description):
        """Wrapping of input resource."""
        input_number = len(self._tb_input) + 1
        self.sh.title('Toolbox input {:02}'.format(input_number))
        try:
            r = toolbox.input(**description)
        except Exception:
            self._notify_inputs_failed()
            raise
        self._tb_input.append(r)
        print(self.ticket.prompt, 'tb input {:02} ='.format(input_number), r)
        print()
        return r

    def _wrapped_promise(self, **description):
        """Wrapping of promised resource."""
        promise_number = len(self._tb_promise) + 1
        self.sh.title('Toolbox promise {:02}'.format(promise_number))
        description['namespace'] = self.output_namespace(description.get('namespace'))
        r = toolbox.promise(**description)
        self._tb_promise.append(r)
        print(self.ticket.prompt, 'tb promise {:02} ='.format(promise_number), r)
        print()
        return r

    def _wrapped_executable(self, **description):
        """Wrapping of executable input."""
        exec_number = len(self._tb_exec) + 1
        self.sh.title('Toolbox executable {:02}'.format(exec_number))
        try:
            r = toolbox.executable(**description)
        except Exception:
            self._notify_inputs_failed()
            raise
        self._tb_exec.append(r)
        print(self.ticket.prompt, 'tb exec {:02} ='.format(exec_number), r)
        print()
        return r

    def _wrapped_output(self, **description):
        """Wrapping of output resource."""
        output_number = len(self._tb_output) + 1
        self.sh.title('Toolbox output {:02}'.format(output_number))
        description['namespace'] = self.output_namespace(description.get('namespace'))
        r = toolbox.output(**description)
        self._tb_output.append(r)
        print(self.ticket.prompt, 'tb output {:02} ='.format(output_number), r)
        print()
        return r


class DavaiTaskMixin(WrappedToolboxMixin):
    """Provide useful methods for Davai IOs."""
    experts = []
    _taskinfo_kind = 'taskinfo'  # Flow taskinfo, can be forced to 'statictaskinfo' for non-flow tasks (e.g. pgd, build...)

    @property
    def lead_expert(self):
        """
        Lead expert is the expert displayed in Ciboulai XP table.
        Default, can still be overwritten in class definition.
        """
        if len(self.experts) > 0:
            return self.experts[0]
        else:
            return None

    @property
    def obs_tslots(self):
        return '/'.join([str(self.conf.timeslots),
                         self.conf.window_start,
                         self.conf.window_length])

    @property
    def NDVar(self):
        return '4DVar' if int(self.conf.timeslots) > 1 else '3DVar'

    @property
    def ND(self):
        return '4D' if int(self.conf.timeslots) > 1 else '3D'

    def guess_term(self, force_window_start=False):
        """Guess term from 'cyclestep' and NDVar or 'force_window_start'."""
        term = Period(self.conf.cyclestep)
        if self.NDVar == '4DVar' or force_window_start:
            # withdraw to window start
            term = term + Period(self.conf.window_start)
        return term.isoformat()

    def _obstype_rundate_association(self):
        """Set 'rundate' as associated with 'obstype' in config (and toolbox defaults)."""
        if 'obstype' in self.conf and 'obstype_rundate_map' in self.conf:
            obstype = self.conf.obstype
            assert obstype in self.conf.obstype_rundate_map, \
                "config file not configurated to loop on obstype '{}' : no rundate associated".format(obstype)
            self.conf.rundate = self.conf.obstype_rundate_map[obstype]
            toolbox.defaults(date=self.conf.rundate)

    def executables_block_gmkpack(self, compilation_flavour=None):
        """
        Return the block in which to find the binaries, wrt self.compilation_flavour or a provided such argument.

        CAREFUL IN MODIFYING THIS: this method is defined to mimic what the loop on compilation flavours does.
        """
        if compilation_flavour is None:
            compilation_flavour = self.conf.compilation_flavour
        return '{}.{}'.format(gmkpack_executables_block_tag, self.conf.compilation_flavour.lower())

    def executables_block(self, **kw):
        """
        Return the block in which to find the binaries, wrt self.compilation_flavour or a provided such argument.
        """
        if self.conf.compiling_system == 'gmkpack':
            return self.executables_block_gmkpack(**kw)
        else:
            raise NotImplementedError("conf.compiling_system == {}".format(self.conf.compiling_system))

    def flow_executable(self, **kw):
        """Shortcut for getting executable from dataflow. Default attributes can be overpassed by argument."""
        description = dict(
            role           = 'Binary',
            block          = self.executables_block(),
            experiment     = self.conf.xpid,
            kind           = 'ifsmodel',
            local          = '{}.X'.format(self.conf.model.upper()),  # legacy nomenclature
            model          = 'ifs',  # as genericly named in cache out of compilation
            nativefmt      = self.conf.executables_fmt,
            )
        description.update(**kw)
        return self._wrapped_executable(**description)

    def run_expertise(self):
        """Run expertise."""
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbexpertise')
            tbexpertise = toolbox.algo(**self._algo_expertise())
            print(self.ticket.prompt, 'tbexpertise =', tbexpertise)
            print()
            self.component_runner(tbexpertise, [None])

    @property
    def taskid(self):
        return self.output_block()

    def output_block(self):
        """
        Output block method: should map more or less Family tree, separated by "-".
        TO BE OVERWRITTEN in (most) real tasks
        """
        return '-'.join([self.tag])

    def _tag_suffix(self):
        """Get the suffix part of the tag, in case of a LoopFamily-ed task."""
        return self.tag[len(self._configtag):]

    def _promised_expertise(self):
        """Standard description of the promised expertise file."""
        return dict(
            role           = 'TaskSummary',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'json',
            hook_train     = (take_the_DAVAI_train,
                              self.conf.expertise_fatal_exceptions,
                              self.conf.hook_davai_wagons),
            kind           = self._taskinfo_kind,
            local          = 'task_summary.[format]',
            namespace      = self.REF_OUTPUT,
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise')

    def _reference_continuity_expertise(self):
        """Standard description of the expertise of the "continuity" reference."""
        return dict(
            role           = 'Reference',
            namespace      = self.conf.ref_namespace,
            experiment     = self.conf.ref_xpid,
            block          = self.output_block(),
            fatal          = False,
            format         = 'json',
            kind           = self._taskinfo_kind,
            local          = 'ref-continuity_summary.[format]',
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise',
            vconf          = self.conf.ref_vconf)

    def _reference_consistency_expertise(self):
        """Standard description of the expertise of the "consistency" reference."""
        return dict(
            role           = 'ConsistencyReference',
            block          = self.consistency_ref_block,
            experiment     = self.conf.xpid,
            fatal          = False,
            format         = 'json',
            kind           = self._taskinfo_kind,
            local          = 'ref-consistency_summary.[format]',
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise')

    def _algo_expertise(self):
        """Standard description of the Expertise AlgoComponent."""
        return dict(
            block          = self.output_block(),
            engine         = 'algo',
            experiment     = self.conf.xpid,
            experts        = self.experts,
            lead_expert    = self.lead_expert,
            fatal_exceptions = self.conf.expertise_fatal_exceptions,
            ignore_reference = self.conf.ignore_reference,
            kind           = 'expertise')

    def _notify_ciboulai(self, step):
        """Notify Ciboulai of a step."""
        from ial_expertise.task import TaskSummary, task_status
        task_summary = TaskSummary()
        if step == 'inputs':
            task_summary['Status'] = task_status['I...']
        elif step == 'inputs:failed':
            task_summary['Status'] = task_status['IF']
        elif step == 'inputs:done':
            task_summary['Status'] = task_status['ID']
        elif step == 'compute':
            task_summary['Status'] = task_status['R...']
        notification_file = '.{}_started.json'.format(step)
        task_summary['Context'] = context_info_for_task_summary(self.ticket.context, jobname=self.conf.jobname)
        task_summary['Updated'] = utcnow().isoformat().split('.')[0]
        task_summary.dump(notification_file)
        description = self._output_expertise()
        description['task'] = step
        description['local'] = notification_file
        description['namespace'] = 'vortex.cache.fr'
        toolbox.output(**description)
        self.ticket.sh.remove(notification_file)

    def _notify_start_inputs(self):
        """Notify Ciboulai that the inputs step has started."""
        if 'early-fetch' in self.steps:
            self._notify_ciboulai('inputs')

    def _notify_inputs_failed(self):
        """Notify Ciboulai that the inputs step has failed."""
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._notify_ciboulai('inputs:failed')

    def _notify_inputs_done(self):
        """Notify Ciboulai that the inputs step has finished."""
        if 'early-fetch' in self.steps:
            self._notify_ciboulai('inputs:done')

    def _notify_start_compute(self):
        """Notify Ciboulai that the compute step has started."""
        if 'compute' in self.steps:
            self._notify_ciboulai('compute')

    def _output_expertise(self):
        """Standard description of the output expertise file."""
        return dict(
            role           = 'TaskSummary',
            kind           = self._taskinfo_kind,
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            hook_train     = (take_the_DAVAI_train,
                              self.conf.expertise_fatal_exceptions,
                              self.conf.hook_davai_wagons),
            format         = 'json',
            local          = 'task_summary.[format]',
            namespace      = self.REF_OUTPUT,
            nativefmt      = '[format]',
            promised       = True,
            scope          = 'itself',
            task           = 'expertise')

    def _output_comparison_expertise(self):
        """Standard description of the output comparison expertise file."""
        return dict(
            role           = 'TaskAgainstRef',
            kind           = self._taskinfo_kind,
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            hook_train     = (take_the_DAVAI_train,
                              self.conf.expertise_fatal_exceptions,
                              self.conf.hook_davai_wagons),
            format         = 'json',
            local          = 'task_[scope].[format]',
            nativefmt      = '[format]',
            scope          = 'continuity,consistency',
            task           = 'expertise')


class DavaiIALTaskMixin(DavaiTaskMixin, IncludesTaskMixin):
    """Provide useful usual outputs for IAL tests."""

    def _reference_continuity_listing(self):
        """Standard description of the listing of the "continuity" reference."""
        return dict(
            role           = 'Reference',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.ref_xpid,
            fatal          = False,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'ref-continuity_listing.[format]',
            namespace      = self.conf.ref_namespace,
            seta           = '1',
            setb           = '1',
            task           = self._configtag,
            vconf          = self.conf.ref_vconf)

    def _reference_consistency_listing(self):
        """Standard description of the listing of the "consistency" reference."""
        return dict(
            role           = 'ConsistencyReference',
            binary         = '[model]',
            block          = self.consistency_ref_block,
            experiment     = self.conf.xpid,
            fatal          = False,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'ref-consistency_listing.[format]',
            namespace      = self.conf.ref_namespace,
            seta           = '1',
            setb           = '1',
            task           = self.consistency_ref_task)

    def _promised_listing(self):
        """
        Standard description of the promised listing.
        Promising it enables to export its cache/archive path to ciboulai.
        """
        return dict(
            role           = 'Listing',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'NODE.001_01',
            namespace      = self.REF_OUTPUT,
            promised       = True,
            seta           = '1',
            setb           = '1',
            task           = self._configtag)

    def _output_listing(self):
        """Standard description of the output listing."""
        return dict(
            role           = 'Listing',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'NODE.{glob:a:\d+}_{glob:b:\d+}',
            namespace      = self.REF_OUTPUT,
            promised       = True,
            seta           = '[glob:a]',
            setb           = '[glob:b]',
            task           = self._configtag)

    def _output_stdeo(self):
        """Standard description of the stdeo.* output files."""
        return dict(
            role           = 'StdOut',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'stdeo.{glob:n:\d+}',
            part           = 'stdeo.[glob:n]',
            task           = self._configtag)

    def _output_drhook_profiles(self):
        """Standard description of the drHook output files."""
        return dict(
            role           = 'DrHookProfiles',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            fatal          = self.conf.drhook_profiling,
            format         = 'ascii',
            kind           = 'drhook',
            local          = 'drhook.prof.{glob:n:\d+}',
            mpi            = '[glob:n]',
            task           = self._configtag)


class BuildMixin(object):
    """A mixin for tasks that deal with building of executables."""

    @property
    def tasks2wait4_file(self):
        """Filepath of witness file listing the build tasks to be waited for."""
        return self.sh.path.join(self.env['HOME'], '.davairc', '.{}.{}'.format(self.conf.xpid, 'buildtasks'))

    def tasks2wait4_rmfile(self):
        """Remove the witness file listing the build tasks to be waited for."""
        if self.sh.path.exists(self.tasks2wait4_file):
            self.sh.rm(self.tasks2wait4_file)

    def tasks2wait4_init(self):
        """(Re-)Initialize the witness file listing the build tasks to be waited for."""
        if self.steps == ('early-fetch',):
            self.tasks2wait4_rmfile()
            with io.open(self.tasks2wait4_file, 'w'):
                pass

    def tasks2wait4_add(self):
        """Add the current task to the witness file listing the build tasks to be waited for."""
        if self.steps == ('early-fetch',):
            with io.open(self.tasks2wait4_file, 'a') as f:
                f.write(self.output_block() + '\n')
                f.flush()

    def tasks2wait4_readlist(self):
        """Read and return the list of build tasks to be waited for."""
        if not self.sh.path.exists(self.tasks2wait4_file):
            # has not been created yet
            return []
        else:
            with io.open(self.tasks2wait4_file, 'r') as f:
                return [l.strip() for l in f.readlines()]


class GmkpackMixin(BuildMixin):
    """A mixin for tasks that deal with building of executables with gmkpack."""

    @property
    def gmkpack_compiler_label(self):
        """Return gmkpack's 'compiler_label' from config's compilation_flavour."""
        return self.conf.compilation_flavour.split('.')[0]

    @property
    def gmkpack_compiler_flag(self):
        """Return gmkpack's 'compiler_flag' from config's compilation_flavour."""
        return self.conf.compilation_flavour.split('.')[1]

    def _guess_pack_from_IAL_git_ref(self, abspath=True, homepack=None, to_bin=True):
        """Guess and return pack according to self.conf"""
        from ial_build.pygmkpack import GmkpackTool
        return GmkpackTool.guess_pack_name(self.conf.IAL_git_ref,
                                           self.gmkpack_compiler_label,
                                           self.gmkpack_compiler_flag,
                                           self.conf.packtype,
                                           IAL_repo_path=self.conf.IAL_repository,
                                           abspath=abspath,
                                           homepack=homepack,
                                           to_bin=to_bin)

    def _guess_pack_from_bundle(self, abspath=True, homepack=None, to_bin=True):
        """Guess and return pack according to self.conf"""
        from ial_build.bundle import IALBundle
        b = IALBundle(self.conf.IAL_bundle_file, src_dir=self.bundle_src_dir)
        return b.gmkpack_guess_pack_name(self.conf.packtype,
                                         self.gmkpack_compiler_label,
                                         self.gmkpack_compiler_flag,
                                         abspath=abspath,
                                         homepack=homepack,
                                         to_bin=to_bin)

    def guess_pack(self, abspath=True, homepack=None, to_bin=True):
        """Guess and return pack according to self.conf"""
        if self.pack_population == 'IAL_git_ref':
            return self._guess_pack_from_IAL_git_ref(abspath=abspath, homepack=homepack, to_bin=to_bin)
        elif self.pack_population == 'IAL_bundle_file':
            return self._guess_pack_from_bundle(abspath=abspath, homepack=homepack, to_bin=to_bin)
        else:
            raise KeyError("Unknown pack_population: ''".format(self.pack_population))

    @property
    def pack_population(self):
        """Guess what the pack has been populated from, according to config."""
        if 'IAL_bundle_file' in self.conf and 'IAL_git_ref' not in self.conf:
            return 'IAL_bundle_file'
        elif 'IAL_git_ref' in self.conf and 'IAL_bundle_file' not in self.conf:
            return 'IAL_git_ref'
        else:
            raise KeyError("One and only one of ('IAL_bundle_file', 'IAL_git_ref') has to be provided in config file")

    @property
    def bundle_src_dir(self):
        if 'bundle_src_dir' in self.conf:
            return os.path.expanduser(os.path.expandvars(self.conf.bundle_src_dir))
        else:
            return None

