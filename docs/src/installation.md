Installation
------------

DAVAI is preinstalled on HPCs clusters at MF and ECMWF.

* on [`belenos`@MF](belenos.md)

* on [`Atos/bologna`@ECMWF](atos_bologna.md)

!!! tip "Useful function to put in your `.bashrc`:"
    ```
    function davai-activate() {
      source ${1:-.}/venv/bin/activate
      }
    ```
    so as to activate an experiment venv using `davai-activate` from within it, or `davai-activate path/to/xp`.

## General installation

You can also setup your own install:
* Create a venv:
  ```
  python -m venv ~/venvs/davai`
  source ~/venvs/davai
  ```
* Then install your own working version, either:
  - Clone this repository, e.g. in `~/repositories/` and install it:
    ```
    git clone https://github.com/ACCORD-NWP/DAVAI.git
    pip install [-e] DAVAI
    ```
  - Or from PyPI:
    ```
    pip install davai
    ```

