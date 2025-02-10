# -*- coding: utf-8 -*-
"""
Canonical Forecasts: with the components they usually embark in operational context
(e.g. inline Fullpos, DDH, sometimes IAU...)
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .canonical.arpege import CanonicalArpegeForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='global798c22', ticket=t, nodes=[
                        CanonicalArpegeForecast(tag='forecast-arpege-global798c22', ticket=t, on_error='delayed_fail', **kw),
                        ], **kw),
                    ], **kw),
            ], **kw),
        ],
    )

