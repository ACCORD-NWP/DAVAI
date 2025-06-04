# DAVAÏ User Guide

DAVAÏ embeds the whole workflow from the source code to the green/red
light validation status: fetching sources from Git, building
executables, running test cases, analysing the results and displaying
them on a dashboard.

For now, the only build system embedded is `gmkpack`, but we expect
other systems to be plugged when required.
The source code to be provided can be either an IAL[^1] Git reference
or an IAL bundle. In the first case, the rest of the projects/repositories
will be infered from the latest official tagged ancestor, using the
git history of IAL-bundle.

The dimensioning of tests (grid sizes, number of observations,
parallelization\...) is done in order to conceal representativity and
execution speed. Therefore, in the general usecases, the tests are
supposed to run on HPC. A dedicated usecase will target smaller
configurations to run on workstation (not available yet).
An accessible source code forge is set within the ACCORD consortium to
host the IAL central repository on which updates and releases are
published, and where integration requests will be posted, reviewed and
monitored.

By the way: DAVAI stands for *"**D**evice **A**iming at the
**VA**lidation of **I**AL"*

[^1]: IAL = **I**FS-**A**rpege-**L**AM
