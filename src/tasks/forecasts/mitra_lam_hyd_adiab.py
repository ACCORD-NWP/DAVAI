# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .mitra.lam import Forecast


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
                    Forecast(tag='L3_FCTI_HYD_EUL_VFD_ADIAB_PGAL', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='L3_FCTI_HYD_SL3_VFD_ADIAB_PGAL', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='L3_FCTI_HYD_SL3_VFE_ADIAB_PGAL', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='L3_FCTI_HYD_SL3_VFD_ADIAB_SLHD_PGAL', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='L3_FCTI_HYD_SL2_VFD_ADIAB_PGAL', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='L3_FCTI_HYD_SL2_VFE_ADIAB_PGAL', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='L3_FCTI_HYD_SL2_VFD_ADIAB_SLHD_PGAL', ticket=t, on_error='delayed_fail', **kw),
                    ],
                **kw
                ),
            ]
        )

