### Jobs & tasks

A *Task* is generally understood as the triplet: 

1. fetch input resources, 
2. run an executable, 
3. dispatch the produced output. 

In a Vortex script, the tasks are written in Python, using classes and functionalities of the Vortex Python packages. In particular, running an
executable is wrapped in what is called an *AlgoComponent*. 
In DAVAÏ, we add a second *AlgoComponent* right after the nominal one in (2) to *"expertise"* the outputs and compare to a reference.

The tasks templates all inherit from the abstract class: `vortex.layout.nodes.Task`. 
A *Test* is a Task that includes an expertise to a reference.
A *Job* is understood as a series of one or several tasks, executed sequentially within one "job submission" to a job scheduler.

The jobs templates are defined as a function `setup` that return a `Driver` object, which itself contains a series of `Task`(s) and `Family`(ies).

In DAVAÏ, the idea is to have the tasks in independent jobs as far as possible, except: for flow-dependent tasks, or for loops on clones of a task with a varying parameter.

