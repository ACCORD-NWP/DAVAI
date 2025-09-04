# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .musc import MUSCForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t, loopconf='compilation_flavours', loopsuffix='.{}', nodes=[
            Family(tag='case_armcu', ticket=t, nodes=[
                # tag must start with model_*
                MUSCForecast(tag='arome_nominal', ticket=t, on_error='delayed_fail', **kw),
                MUSCForecast(tag='arome_nosfx', ticket=t, on_error='delayed_fail', **kw),
                MUSCForecast(tag='arpege_nominal', ticket=t, on_error='delayed_fail', **kw),
                MUSCForecast(tag='arpege_nosfx', ticket=t, on_error='delayed_fail', **kw),
                ], **kw),
            ], **kw),
        ],
    )
