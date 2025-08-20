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
                    Forecast(tag='L3_FCTI_NHE_EUL_VFD_ADIAB_FROC', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='L3_FCTI_NHE_SL3_VFD_ADIAB_RDBBC2_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCTI_NHE_SL2_VFD_ADIAB_RDBBC2_PCC_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCTI_NHE_SL2_VFD_ADIAB_RDBBC2_PCF_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCTI_NHE_SL2_VFD_ADIAB_GWADV2_PCC_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCTI_NHE_SL2_VFD_ADIAB_GWADV2_PCF_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCTI_NHE_SL2_VFE_ADIAB_GWADV2_PCF_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCTI_NHE_SL2_VFD_ADIAB_NGWADV2_PCF_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCTI_NHE_SL2_VFE_ADIAB_NGWADV2_PCF_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCST_NHE_SL2_VFD_ADIAB_GWADV2_PCC_FROC', ticket=t, on_error='delayed_fail', **kw),
                    #Forecast(tag='L3_FCST_NHE_SL2_VFD_ADIAB_GWADV5_PCF_FROC', ticket=t, on_error='delayed_fail', **kw),
                    ],
                **kw
                ),
            ]
        )

