# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver, Family, LoopFamily

from davai.vtx.tasks.mixins import DavaiTaskMixin, BundleMixin
from ial_build.bundle import TmpIALbundleRepo
from git import Repo
import os
import shutil
def setup(t, **kw):
    return Driver(tag='build', ticket=t, options=kw, nodes=[
        Family(tag='bundle', ticket=t, nodes=[
            LoopFamily(tag='loop_g2p', ticket=t,
                loopconf='compilation_flavours',
                loopsuffix='.{}',
                nodes=[
                    BundleCreate(tag='bundle_create', ticket=t, **kw)
                ], **kw),
            ], **kw),
        ],
    )


class BundleCreate(Task, DavaiTaskMixin, BundleMixin):

    def process(self):
        self._wrapped_init()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            if 'IAL_bundle_repository' in self.conf:
                repo_url=self.conf.get("IAL_bundle_repository")
                ref=self.conf.get("IAL_bundle_ref")
                if os.path.isdir(self.bundle_dir):
                    shutil.rmtree(self.bundle_dir)
                print(f" Cloning repository from {repo_url} into {self.bundle_dir} ...")
                repo = pygit2.clone_repository(repo_url,self.bundle_dir,checkout_branch=ref)
                print(f" Successfully cloned and checked out to '{ref}' in '{self.bundle_dir}'.")
            
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.2/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.2/ Compute step
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                build_dir = self.bundle_xp_build_dir,
                bundle_src_dir = self.conf.get("bundle_src_dir"),
                bundle_dir = self.bundle_dir,
                bundle_file   = self.conf.get("IAL_bundle_file"),
                update_git_repositories = self.conf.get("update_git_repositories"),
                gh_token_file = self.conf.get("gh_token_file"),
                gh_connection = self.conf.get("gh_connection"),
                crash_witness  = False,
                engine         = 'algo',
                kind           = 'bundlecreate',
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, [None])
            ###-------------------------------------------------------------------------------
            ###-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

