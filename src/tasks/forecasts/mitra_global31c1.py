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
                    Forecast(tag='GM_FCST_HYD_EUL_VFD_ADIAB_TL031U', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_EXTCLA_VESL_TL031U', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_EXTCLA_XIDT_TL031U', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_VESL_TL031U', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_TL031U', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL3_VFD_ADIAB_TL031U', ticket=t, on_error='delayed_fail', **kw),
                    ],
                **kw
                ),
            ]
        )

