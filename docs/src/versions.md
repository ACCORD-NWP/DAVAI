Versions
--------

There are two possible reasons to release new versions of the tests:
- evolutions of the testing machinery, for technical reasons, or to add new tests
- evolutions required by changes in the IAL and/or other NWP packages (OOPS, etc).
  Note in particular that the id of the reference experiment (i.e. the experiment to which results are compared to) is registered in the config file.
  A modification in the IAL that changes numerical results requires a new reference experiment.

From commit 9c21941c of IAL, integrated at the beginning of CY50T1, a default version of the tests is registered in the IAL repository,
which will be updated to indirectly refer to the reference experiment to be used for anything based on that same version of the IAL.
Specifying the davai version when creating an experiment then becomes optional, infered from the IAL when possible.

Versions from 2.0.0
===================

| Davai version | IAL Cycle of reference experiment | Note |
|:--------------|:----------------------------------|:-----|
| 2.0.0 | CY50 | Warning: issue with `davai-new_xp_from_bundle` |
| 2.0.1 | CY50 | |
| DV50_T1rc.02 | CY50_T1rc.02 | |
