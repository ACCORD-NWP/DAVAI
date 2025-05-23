# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .standalone.arome import StandaloneAromeForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='corsica2500', ticket=t, nodes=[
                        StandaloneAromeForecast(tag='arome_nominal', ticket=t, **kw),
                        StandaloneAromeForecast(tag='arome_nproma32', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
        ],
    )

