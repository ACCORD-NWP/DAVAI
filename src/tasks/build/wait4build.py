# -*- coding: utf-8 -*-
import sys
import footprints.util
import time
from collections import OrderedDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

import common

from davai.vtx.tasks.mixins import BuildMixin


def setup(t, **kw):
    return Driver(
        tag     = 'setup',
        ticket  = t,
        nodes   = [
            Wait4Build(tag='wait4build', ticket=t, **kw),
        ],
        options=kw
    )


class Wait4BuildInit(Task, BuildMixin):
    """(Re-)Initialize list of tasks to be waited for. This list is completed by step 01 of actual build tasks."""

    def process(self):
        self.tasks2wait4_init()


class Wait4Build(Task, BuildMixin):
    """Wait for build tasks to finish."""

    _taskinfo_kind = 'statictaskinfo'

    @property
    def _expertise_description(self):
        return dict(
            kind           = self._taskinfo_kind,
            cutoff         = 'assim',
            experiment     = self.conf.xpid,
            format         = 'json',
            local          = 'compilation_output.[format]',
            namespace      = 'vortex.cache.fr',
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise')

    def _expertise_available(self, start_of_run, **expertise_description):
        """Check if expertise is available and posterior to run start."""
        ok = False
        rh = toolbox.rload(**expertise_description)[0]
        exists = bool(rh.check())
        path = rh.locate().split(';')[0]
        #print(path, exists)
        if exists:
            last_modified_time = self.sh.path.getmtime(path)
            #print(last_modified_time)
            if last_modified_time > start_of_run:
                ok = True
        return ok

    def _check_build(self, expertise_rh):
        """Check in expertise if task succeeded."""
        expertise = expertise_rh.contents.data
        task_OK = expertise['Status']['short'].startswith('Ended')
        if not task_OK:
            print("Task failed:", expertise['Exception'])
            exit(1)

    def _get_expertise(self, **expertise_description):
        """Get expertise, waiting for it if necessary."""
        t = self.ticket
        sh = self.sh
        # timings
        start_of_run = float(self.sh.environ.get('DAVAI_START_BUILD', time.time()))
        walltime = self.conf.time
        # get compilation task time (e.g. 02:00:00) in seconds
        walltime_in_seconds = sum([60**(2-i) * int(v)
                                   for i,v in enumerate(walltime.split(':'))]
                                  ) + 600  # a large 10 mins margin for step.01 of packbuild
        walltime += '(+ 10:00 margin for queueing)'
        print("Begin waiting for '{}' expertise, for up to".format(expertise_description['block']),
              "{} == {} seconds".format(walltime, walltime_in_seconds))
        # start waiting for expertise
        initial_walltime = walltime_in_seconds
        while not self._expertise_available(start_of_run, **expertise_description):
            # wait for compilation expertise to be present in cache
            status = 'Waiting time: {:5d}/{:5d}s'.format(initial_walltime - walltime_in_seconds, initial_walltime)
            if walltime_in_seconds <= 0:
                print("Could not get expertise after supposed maximum Elapsed time: check manually. Exit")
                exit(-1)
            elif walltime_in_seconds < initial_walltime:
                sys.stdout.write('\b' * len(status))
                sys.stdout.flush()
            sys.stdout.write(status)
            sys.stdout.flush()
            time.sleep(int(self.conf.refresh_frequency))
            walltime_in_seconds -= int(self.conf.refresh_frequency)
        else:
            # expertise available: continue
            print("\nExpertise available !")
            # fetch it
            expertise = toolbox.input(**expertise_description)
            print(t.prompt, 'expertise =', expertise)
        return expertise[0]

    def task2wait4(self):
        tasks = self.tasks2wait4_readlist()
        # make them unique but keeping order
        tasks = list(OrderedDict.fromkeys(tasks))
        for t in self._tasks_done:
            if t in tasks:
                tasks.remove(t)
        if len(tasks) > 0:
            return tasks[0]
        else:
            return None

    def process(self):
        self._tasks_done = []
        #for block in self.conf.wait4steps:
        while len(self._tasks_done) == 0 or self.task2wait4() is not None:
            # beginning: no task registered yet and done == 0
            cpt = 0
            while self.task2wait4() is None and len(self._tasks_done) == 0:
                status = '{:3d}s'.format(cpt * int(self.conf.refresh_frequency))
                if cpt == 0:
                    print("Build tasks have not started yet, waiting for them...")
                    #print("Build tasks have not started yet, wait another {}s for them...".format(self.conf.refresh_frequency))
                else:
                    sys.stdout.write('\b' * len(status))
                    sys.stdout.flush()
                sys.stdout.write(status)
                sys.stdout.flush()
                time.sleep(int(self.conf.refresh_frequency))
                cpt += 1
            print("\n... build tasks started.")
            # here's the next task to wait for
            task = self.task2wait4()
            # get compilation expertise
            expertise = self._get_expertise(block=task, **self._expertise_description)
            # then remember this task has been done
            self._tasks_done.append(task)
            # check that all builds are successful
            self._check_build(expertise)
            # and loop if there are still tasks to wait
        print("All build tasks have finished:")
        for t in self._tasks_done:
            print("- {}".format(t))
        # finally, remove list-of-tasks file
        self.tasks2wait4_rmfile()

