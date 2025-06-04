# Update namelists for Davai

In this example, we need to update namelists of Davai for the needs of a code modification
(e.g. renaming of a variable, or adding a new block).

We can do this in 2 ways:

## Changing on-the-fly when fetching the namelist before execution

*In this case, you need to be in __editable mode__, cf. [Run tests](runtests.md).*

- Edit the task where you want to do the change, e.g. `DAVAI/src/tasks/forecasts/standalone/alaro.py`
- Look for the section where the namelist (fort.4) is fetched
- Decomment its `hook_z` attribute
- Set the values you need using python syntax

## Changing the stored and historised namelist

Cf. dedicated page [here](uget/update_namelists.md)

