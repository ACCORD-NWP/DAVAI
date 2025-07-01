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
                    Family(tag='alaro0', ticket=t, nodes=[
                        StandaloneAlaroForecast(tag='aplpar', on_error='delayed_fail', ticket=t, **kw),
                        StandaloneAlaroForecast(tag='apl_alaro', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
        ],
    )

