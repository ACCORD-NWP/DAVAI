# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .standalone.alaro import StandaloneAlaroForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='antwrp1300', on_error='delayed_fail', ticket=t, nodes=[
                    StandaloneAlaroForecast(tag='alaro0', on_error='delayed_fail', ticket=t, **kw),
                    StandaloneAlaroForecast(tag='alaro1', ticket=t, **kw),
                    ], **kw),
                ], **kw),
        ],
    )

