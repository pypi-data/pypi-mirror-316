======================
Neural Network Figures
======================

Copyright (c) 2017-2024 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)

* Web site: https://gitlab.com/jdhp-dev/neural-network-figures
* Online documentation: https://jdhp-dev.gitlab.io/neural-network-figures
* Source code: https://gitlab.com/jdhp-dev/neural-network-figures
* Issue tracker: https://gitlab.com/jdhp-dev/neural-network-figures/issues
* Pytest code coverage: https://jdhp-dev.gitlab.io/neural-network-figures/htmlcov/index.html
* Neural Network Figures on PyPI: https://pypi.org/project/nnfigs


Table of Contents
=================

.. contents::
   :depth: 2


Description
===========

Draw neural network figures with Matplotlib

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

Neural Network Figures requires Python 3.11 (or newer) and Python packages listed in the `requirements.txt` file.


.. _install:

Installation (development environment)
======================================

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the Neural Network Figures source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Windows
-------

From the Neural Network Figures source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Installation (production environment)
=====================================

::

    pip install nnfigs


Documentation
=============

* Online documentation: https://jdhp-dev.gitlab.io/neural-network-figures
* API documentation: https://jdhp-dev.gitlab.io/neural-network-figures/api.html


Build and run the Python Docker image
=====================================

Build the docker image
----------------------

From the Neural Network Figures source code::

    docker build -t nnfigs:latest .

Run unit tests from the docker container
----------------------------------------

From the Neural Network Figures source code::

    docker run nnfigs pytest

Run an example from the docker container
----------------------------------------

From the Neural Network Figures source code::

    docker run nnfigs python3 /app/examples/hello.py


Bug reports
===========

To search for bugs or report them, please use the Neural Network Figures Bug Tracker at:

    https://gitlab.com/jdhp-dev/neural-network-figures/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe