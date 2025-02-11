# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver, Family, LoopFamily

from davai.vtx.tasks.mixins import DavaiTaskMixin, GmkpackMixin


def setup(t, **kw):
    return Driver(tag='build', ticket=t, options=kw, nodes=[
        Family(tag='gmkpack', ticket=t, nodes=[
            LoopFamily(tag='loop_g2p', ticket=t,
                loopconf='compilation_flavours',
                loopsuffix='.{}',
                nodes=[
                    Bundle2Pack(tag='bundle2pack', ticket=t, **kw)
                ], **kw),
            ], **kw),
        ],
    )


class Bundle2Pack(Task, DavaiTaskMixin, GmkpackMixin):

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
            bundle_provider = dict()
            if self.conf.get('IAL_bundle_file', None):
                bundle_provider['remote'] = self.conf.IAL_bundle_file
            else:
                # TODO: use git provider when available
                IALbundles = TmpIALbundleRepo(self.conf.IAL_bundle_repository, verbose=True)
                b = IALbundles.get_bundle(self.IAL_bundle_ref, to_file='__tmp__')
                bundle_provider['remote'] = b.bundle_file
            self._wrapped_input(
                role           = 'Bundle',
                nativefmt      = 'yml',
                kind           = 'bundle',
                #shouldfly      = True,
                local          = 'bundle.yml',
                **bundle_provider,
            )
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
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                bundle_src_dir = self.bundle_src_dir,
                cleanpack      = self.conf.get('cleanpack', False),
                compiler_flag  = self.gmkpack_compiler_flag,
                compiler_label = self.gmkpack_compiler_label,
                crash_witness  = False,
                engine         = 'algo',
                homepack       = self.conf.get('homepack', None),
                kind           = 'bundle2pack',
                pack_type      = self.conf.packtype,
                preexisting_pack = self.conf.preexisting_pack,
                rootpack       = self.conf.get('rootpack', None)
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, [None])
            #-------------------------------------------------------------------------------
            #-------------------------------------------------------------------------------

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

