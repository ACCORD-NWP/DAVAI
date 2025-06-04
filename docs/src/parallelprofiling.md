## Parallel profiling

Each job has a section in the config file, in which one can tune the
requested profile parameters to the jobs scheduler:

-   `time` : elapse time

-   `ntasks` : number of MPI tasks per node

-   `nnodes` : number of nodes

-   `openmp` : number of OpenMP threads

-   `partition` : category of nodes

-   `qos` : quality of service (nodes)

-   `mem` : memory (helps to prevent OOM)

The total number of MPI tasks is therefore `nnodes \times ntasks`, and
is automatically replaced in namelist

