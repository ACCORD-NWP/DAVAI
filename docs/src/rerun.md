### Re-run a test

The Davai command `davai-run_tests` launches all the jobs listed in
`conf/<USECASE>.yaml`, sequentially and independently (i.e. without
waiting for the jobs to finish). The command can also be used
complementary:

-   to list the jobs that would be launched by the command, according to
    the `conf/<USECASE>.yaml` config file:
    ```
    davai-run_tests -l
    ```

-   to run a single job:

    ```
    davai-run_tests -j <job identifier as given by -l option>
    ```

Some tests are gathered together within a single job. There are 2
reasons for that: if they are an instance of a loop (e.g. same test on
different obstypes, or different geometries), or if they have a
flow-dependency with an upstream/downstream test (e.g. `bator >
screening > minimization`).

When a test fails within a job and the user wants to re-run it without
re-runnning the other tests from the same job, it is possible to do so
by deactivating them[^1] :

-   **loops:** to deactivate members of a loop:
    open config file `conf/davai_.ini`, and in the section corresponding
    to the job or family, the loops can be found as `list(...)`, e.g.
    `obstypes`, `rundates` or `geometries`. Items in the list can be
    reduced to the only required ones (note that if only one item
    remains, one needs to keep a final `","` within the parenthesis).

-   **dependency:** open driver file corresponding to the job name in
    `tasks/` directory, and comment out (`#`) the unrequired tasks or
    families of *`nodes`*, leaving only the required task.

[^1]: including upstream tasks that produce flow-resources for the
    targeted test, as long as the resources stay in cache
