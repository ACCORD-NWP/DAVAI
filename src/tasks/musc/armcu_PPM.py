# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .pgd import MUSC_PGD as PGD
from .prep import MUSCPrep as Prep
from .musc import MUSCForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='models', ticket=t,
            loopconf='model_configs',
            loopsuffix='.{}',
            nodes=[
                Family(tag='case_armcu', ticket=t, on_error='delayed_fail', nodes=[
                    PGD(tag='pgd', ticket=t, **kw),
                    Prep(tag='prep', ticket=t, **kw),
                    LoopFamily(tag='gmkpack', ticket=t,
                        loopconf='compilation_flavours',
                        loopsuffix='.{}',
                        nodes=[
                            MUSCForecast(tag='model', ticket=t, on_error='delayed_fail', **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
        ],
    )
