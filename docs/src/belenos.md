Complementary information about DAVAI setup on `belenos` HPC machine @ MF
=========================================================================

Quick install
-------------

Set in your `.bash_profile`:
```bash
module use ~mary/public/modulefiles
```

then when you need to load davai to create a new testing experiment:
```bash
module load davai/2.0.0
```

Note: the version of the tests used in your experiment can be different from the version loaded here.
This `module load ...` is only useful to prepend the PATH with `davai-new_xp*` command(s).

---

Pre-requirements
----------------

1. Load modules (conveniently in your `.bash_profile`):
   ```
   module load python/3.10.12
   module load git
   ```

2. Configure your `~/.netrc` file for FTP communications with archive machine hendrix, if not already done:
   ```
   machine hendrix login <your_user> password <your_password>
   machine hendrix.meteo.fr login <your_user> password <your_password>
   ```
   (! don't forget to `chmod 600 ~/.netrc` if you are creating this file !)\
   _To be updated when you change your password_

3. Configure ftserv (information is stored encrypted in ~/.ftuas):\
   `ftmotpasse -h hendrix -u <your_user>`\
   (and give your actual password)\
   **AND**\
   `ftmotpasse -h hendrix.meteo.fr -u <your_user>`\
   (same)\
   _To be updated when you change your password_

4. Configure Git proxy certificate info :\
   `git config --global http.sslVerify false`

5. Ensure SSH connectivity between compute and transfer nodes, if not already done:\
   `cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys`

