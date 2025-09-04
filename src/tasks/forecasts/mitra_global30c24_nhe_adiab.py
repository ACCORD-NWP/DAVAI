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
                    Forecast(tag='GM_FCST_NHE_SL2_VFD_ADIAB_GWADV5_SI_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_EUL_VFD_ADIAB_PCF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_EUL_VFD_ADIAB_SI_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFD_ADIAB_GWADV2_PCC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFD_ADIAB_GWADV2_PCF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFD_ADIAB_GWADV2_SI_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFD_ADIAB_NGWADV2_PCF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFD_ADIAB_RDBBC2_PCC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFD_ADIAB_RDBBC2_PCF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFD_ADIAB_RDBBC2_SI_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFE_ADIAB_GWADV2_PCC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFE_ADIAB_GWADV2_PCF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL2_VFE_ADIAB_NGWADV2_PCF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_NHE_SL3_VFD_ADIAB_RDBBC2_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    ],
                **kw
                ),
            ]
        )

