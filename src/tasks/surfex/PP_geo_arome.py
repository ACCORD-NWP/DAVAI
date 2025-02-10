# -*- coding: utf-8 -*-
"""
PP_geo = PGD+Prep on a range of LAM geometries
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from tasks.surfex.pgd import PGD
from tasks.surfex.prep import Prep


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                Family(tag='arome_physiography', ticket=t, nodes=[
                    LoopFamily(tag='lam_geometries', ticket=t,
                        loopconf='geometrys',
                        loopsuffix='-{0.tag}',
                        nodes=[
                        Family(tag='PP-aro', ticket=t, on_error='delayed_fail', nodes=[
                            PGD(tag='pgd-arome', ticket=t, **kw),
                            Prep(tag='prep-arome', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

