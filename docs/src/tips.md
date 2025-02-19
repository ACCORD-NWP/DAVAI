### First tips

- All Davai commands are prefixed `davai-*` and can be listed with `davai-help`. All commands are auto-documented with option `-h`.
- If the **pack preparation or compilation fails**, for whatever reason, the build step prints an error message and the `davai-run_xp` command stops before running the tests. You can find the output of the pack preparation or compilation in `logs/` directory, as any other test log file.

  A very common error is when the pack already exists; if you actually want to overwrite the contents of the pack (e.g. because you just fixed a code issue in the branch), you may need option `-e/–preexisting_pack`:

    ```
    davai-run_xp -e
    ```

    or

    ```
    davai-build -e
    ```

    Otherwise, if the pack preexists independently for valid reasons, you will need to move/delete the existing pack, or rename your branch.

- The tests are organised as **tasks** and **jobs**:

  - a **task** consists in fetching input resources, running an executable, analyzing its outputs to the Ciboulai dashboard and dispatching (archiving) them: *1 test = 1 task*
  - a **job** consists in a sequential driver of one or several *task(s)*: either a flow sequence (i.e. outputs of task N is an input of task N+1) or family sequence (e.g. run independently an IFS and an Arpege forecast)

- To **fix a piece of code**, the best is to modify the code in your Git repo, then re-run

  ```
  davai-run_xp -e
  ```
  (or `davai-build -e` and then `davai-run_tests`).

  You don't necessarily need to commit the change rightaway, the
  non-committed changes are exported from Git to the pack. Don't
  forget to commit eventually though, before issuing pull request.

- To **re-run one job only after re-compilation**, type

  ```
  davai-run_tests -l
  ```
  
  to list the jobs and then

  ```
  davai-run_tests -j <category.job>
  ```
  
  !!! note "Example" 
      ```
      davai-run_tests -j forecasts.standalone_forecasts
      ```

- The syntax `category.job` indicates that the job to be run is the **Driver** in `./tasks/category/job.py`
- To **re-run a single test** within a job, e.g. the IFS forecast in `forecasts/standalone_forecasts.py`: edit this file, comment the other `Family`(s) or `Task`(s) (*nodes*) therein, and re-run the job as indicated above.

- **Eventually**, after code modifications and fixing particular tests, you should re-run **the whole set of tests**, to make sure your fix does not break any other test.

