# -*- coding: utf-8 -*-
"""
PPF = PGD-Prep-Forecast (to test an update of Surfex PGD and IC files, in the dataflow)
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from tasks.surfex.pgd import PGD
from tasks.surfex.prep import Prep
from tasks.forecasts.standalone.arpege import StandaloneArpegeForecast
from tasks.forecasts.standalone.arome import StandaloneAromeForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                Family(tag='corsica2500', ticket=t, nodes=[
                    Family(tag='arome_physiography', ticket=t, nodes=[
                        PGD(tag='pgd-arome-corsica2500', ticket=t, **kw),
                        ], **kw),
                    Prep(tag='prep-arome-corsica2500', ticket=t, **kw),
                    StandaloneAromeForecast(tag='forecast-arome-corsica2500', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                Family(tag='globaltst149c24', ticket=t, nodes=[
                    Family(tag='arpege_physiography', ticket=t, nodes=[
                        PGD(tag='pgd-arpege-globaltst149c24', ticket=t, **kw),
                        ], **kw),
                    Prep(tag='prep-arpege-globaltst149c24', ticket=t, **kw),
                    StandaloneArpegeForecast(tag='forecast-arpege-globaltst149c24', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

