# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

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
                    Forecast(tag='GM_FCTI_NHQ_SL2_VFD_ARPPHYISBA_GWADV2_PCC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHQ_SL2_VFD_ARPPHYISBA_GWADV2_PCF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    ],
                **kw
                ),
            ]
        )

