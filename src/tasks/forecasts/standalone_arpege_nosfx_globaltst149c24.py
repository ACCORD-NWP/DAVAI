# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver, LoopFamily
from common.util.hooks import update_namelist
import davai

from .standalone.arpege import StandaloneArpegeForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='globaltst149c24', ticket=t, nodes=[
                        StandaloneArpegeForecast(tag='forecast-arpege_nosfx-globaltst149c24', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
        ],
    )

