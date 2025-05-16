# -*- coding: utf-8 -*-

import vortex
from vortex.layout.nodes import Task, Driver, Family, LoopFamily

from davai.util import gmkpack_executables_block_tag
from .pack2bin import Pack2Bin
from ..wait4build import Wait4BuildInit


def setup(t, **kw):
    return Driver(tag='build', ticket=t, options=kw, nodes=[
        Wait4BuildInit(tag='wait4build_init', ticket=t, **kw),  # (re-)initialize list of tasks to be waited for
        Family(tag='gmkpack', ticket=t, nodes=[
            LoopFamily(tag='loop_g2p', ticket=t,
                loopconf='compilation_flavours',
                loopsuffix='.{}',
                nodes=[
                    Pack2Bin(tag=gmkpack_executables_block_tag, ticket=t, **kw),
                ], **kw),
            ], **kw),
        ],
    )

