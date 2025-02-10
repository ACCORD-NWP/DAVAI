# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver, LoopFamily
from common.util.hooks import update_namelist
import davai

from .standalone.arome import StandaloneAromeForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='corsica2500', ticket=t, nodes=[
                        StandaloneAromeForecast(tag='forecast-arome-corsica2500', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
        ],
    )

