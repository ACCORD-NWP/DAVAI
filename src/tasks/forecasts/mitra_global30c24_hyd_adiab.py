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
                    Forecast(tag='GM_FCST_HYD_EUL_VFD_ADIAB_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_RVFE_ADIAB_SETTLS_NDEC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_EXTCLA_VESL_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_EXTCLA_XIDT_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_PCF_NDEC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_VESL_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_MSLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_NDPSFI_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_OSLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_RW2TLFF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SPRTGPQ_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SPRTSPQ_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SSLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFE_ADIAB_SETTLS_NDEC_RW2TLFF_RFRIC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL2_VFE_ADIAB_SETTLS_NDEC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCST_HYD_SL3_VFD_ADIAB_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_EUL_VFD_ADIAB_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_RVFE_ADIAB_SETTLS_NDEC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_EXTCLA_VESL_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_EXTCLA_XIDT_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_PCF_NDEC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_VESL_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_MSLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_NDPSFI_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_OSLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_RW2TLFF_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SPRTGPQ_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SPRTSPQ_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_SSLHD_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFD_ADIAB_SETTLS_XIDT_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFE_ADIAB_SETTLS_NDEC_RW2TLFF_RFRIC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL2_VFE_ADIAB_SETTLS_NDEC_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    Forecast(tag='GM_FCTI_HYD_SL3_VFD_ADIAB_TL030S', ticket=t, on_error='delayed_fail', **kw),
                    ],
                **kw
                ),
            ]
        )

