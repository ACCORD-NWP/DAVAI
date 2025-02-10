# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .bmat.BmatSimple import Bmat as BmatSimple
from .bmat.BmatFlowDependent import Bmat as BmatFlowDependent
from .bmat.EnsembleRead import EnsembleRead as EnsembleRead
from .bmat.EnVarAdjoint import EnVarAdjoint as EnVarAdjoint

def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='4dvar6h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    BmatSimple(tag='BmatSp', ticket=t, **kw),
                    BmatFlowDependent(tag='BmatWv', ticket=t, **kw),
                    EnVarAdjoint(tag='EnVarAdjoint', ticket=t, **kw),
                    LoopFamily(tag='ensread', ticket=t,
                        loopconf='mpireads',
                        loopsuffix='-mpi{}',
                        nodes=[
                        Family('EnsRead', ticket=t, on_error='delayed_fail', nodes=[
                            EnsembleRead(tag='EnsembleRead', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

