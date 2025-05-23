# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .standalone.alaro import StandaloneAlaroForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='chmh2325', ticket=t, on_error='delayed_fail', nodes=[
                    StandaloneAlaroForecast(tag='alaro1sfx', ticket=t, **kw),
                    ], **kw),
                ], **kw),
        ],
    )

