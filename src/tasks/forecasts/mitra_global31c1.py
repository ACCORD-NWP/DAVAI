# -*- coding: utf-8 -*-

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Family, Driver, LoopFamily
from common.util.hooks import update_namelist
import davai

from .mitra.arpege import Forecast


def setup(t, **kw):
    return Driver(
        tag='drv',
        ticket=t,
        options=kw,
        nodes=[
            LoopFamily(
                tag='gmkpack',
                ticket=t,
                loopconf='compilation_flavours',
                loopsuffix='.{}',
                nodes=[
                    Forecast(tag='GM_FCTI_HYD_EUL_VFD_ARPPHYISBA_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL3_VFD_ARPPHYISBA_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    ],
                **kw
                ),
            ]
        )

