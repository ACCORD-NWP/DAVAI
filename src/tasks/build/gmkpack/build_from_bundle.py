# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, LoopFamily, Family

from .bundle2pack import Bundle2Pack
from .pack2bin import Pack2Bin
from tasks.build.wait4build import Wait4BuildInit

from davai.vtx.tasks import gmkpack_executables_block_tag


def setup(t, **kw):
    return Driver(
        tag     = 'build',
        ticket  = t,
        nodes   = [
            Wait4BuildInit(tag='wait4build_init', ticket=t, **kw),  # (re-)initialize list of tasks to be waited for
            Family(tag='gmkpack', ticket=t, nodes=[
                # Two loops rather than one with both tasks in, so that packs are created anyway if compilation fails
                LoopFamily(tag='loop_b2p', ticket=t,
                    loopconf='compilation_flavours',
                    loopsuffix='.{}',
                    nodes=[
                        Bundle2Pack(tag='bundle2pack', ticket=t, **kw),
                    ], **kw),
                LoopFamily(tag='loop_p2b', ticket=t,
                    loopconf='compilation_flavours',
                    loopsuffix='.{}',
                    nodes=[
                        Pack2Bin(tag=gmkpack_executables_block_tag, ticket=t, **kw)
                    ], **kw),
            ], **kw),
        ],
        options=kw
    )

