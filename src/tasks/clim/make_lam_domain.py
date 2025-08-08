# -*- coding: utf-8 -*-

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver
from common.util.hooks import update_namelist
import davai

from davai.vtx.tasks.mixins import DavaiIALTaskMixin, IncludesTaskMixin


class MakeLamDomain(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = []  # [FPDict({'kind':'fields_in_file'})]
    _taskinfo_kind = 'statictaskinfo'

    def geom_params(self):
      if self.conf.geometry.tag == 'nm2500':
        gp =  {'Iwidth':8,'Xpoints_CI':181,'Ypoints_CI':97,'center_lat':7.,'center_lon':80.,'force_projection':'mercator','maximize_CI_in_E':False,'reference_lat':None,'resolution':2500,'tilting':0}
      elif self.conf.geometry.tag == 'sm2500':
        gp =  {'Iwidth':8,'Xpoints_CI':181,'Ypoints_CI':97,'center_lat':-1.,'center_lon':-78.,'force_projection':'mercator','maximize_CI_in_E':False,'reference_lat':None,'resolution':2500,'tilting':0}
      elif self.conf.geometry.tag == 'nlcc2500':
        gp =  {'Iwidth':8,'Xpoints_CI':97,'Ypoints_CI':181,'center_lat':8.5,'center_lon':43.,'force_projection':'lambert','maximize_CI_in_E':False,'reference_lat':None,'resolution':2500,'tilting':0}
      elif self.conf.geometry.tag == 'slcc2500':
        gp =  {'Iwidth':8,'Xpoints_CI':181,'Ypoints_CI':97,'center_lat':-42,'center_lon':146.,'force_projection':'lambert','maximize_CI_in_E':False,'reference_lat':None,'resolution':2500,'tilting':0}
      elif self.conf.geometry.tag == 'nps2500':
        gp =  {'Iwidth':8,'Xpoints_CI':181,'Ypoints_CI':97,'center_lat':78.,'center_lon':16.,'force_projection':'polar_stereographic','maximize_CI_in_E':False,'reference_lat':None,'resolution':2500,'tilting':0}
      elif self.conf.geometry.tag == 'sps2500':
        gp =  {'Iwidth':8,'Xpoints_CI':181,'Ypoints_CI':97,'center_lat':-66.,'center_lon':140.,'force_projection':'polar_stereographic','maximize_CI_in_E':False,'reference_lat':None,'resolution':2500,'tilting':0}
      else:
        raise Exception("Unknown geometry: ",self.conf.geometry.tag)
      return(gp)

    def process(self):
        self._wrapped_init()
        self._notify_start_inputs()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #self._wrapped_promise(**self._promised_expertise())
            pass
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
          pass  # not so useful to compare namelist to reference

            #-------------------------------------------------------------------------------

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._load_usual_tools()  # LFI tools, ecCodes defs, ...
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            pass

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            #-------------------------------------------------------------------------------
            pass

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        self._notify_inputs_done()
        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                e_zone_in_pgd  = True,
                engine         = 'algo',
                format         = '',
                geom_params     = self.geom_params(),
                geometry        = self.conf.geometry.tag,
                i_width_in_pgd = True,
                illustration   = False,
                intent         = '',
                kind           = 'make_lam_domain',
                mode           = 'center_dims',    # 'center_dims' or 'lonlat_included'
                orography_truncation = 'quadratic', # 'linear', 'quadratic' or 'cubic'
                truncation = 'linear',
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, [None])
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            #-------------------------------------------------------------------------------
            self._wrapped_output(
              role           = 'Namelist',
              #block          = c2v(e.CLASS),
              block = self.output_block(),
              #experiment     = c2v(e.XPID),
              experiment = self.conf.xpid,
              format         = 'ascii',
              geometry       = '[glob:g]',
              kind           = 'geoblocks',
              local          = '{glob:g:\w+}.namel_{glob:n:\w+}.geoblocks',
              namespace      = self.REF_OUTPUT,
              target         = '[glob:n]',
            )
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            #self._wrapped_output(**self._output_comparison_expertise())
            pass
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            #self._wrapped_output(**self._output_listing())
            pass
            #-------------------------------------------------------------------------------

