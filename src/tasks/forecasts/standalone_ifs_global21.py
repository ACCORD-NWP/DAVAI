# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .standalone.ifs import StandaloneIFSForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='ifs', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='global21', ticket=t, nodes=[
                        StandaloneIFSForecast(tag='forecast', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
        ],
    )

