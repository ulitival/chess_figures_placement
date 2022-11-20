:Authors:
    Valerii Ulitin
:Version: 1.0 of 2022/11/20

Chess figures placement aka N-knights, N-bishops, N-rooks, N-queens problem.
============================================================================

Known limitations for the current solution.
-------------------------------------------

For the *N-knight* problem, the CSP solution, unfortunately, cannot find a feasible solution within an acceptable time.
I run some test and for ``N=7`` and ``N=8`` I wasn't able to get the result in a few hours. Although, we can utilise
a known values for ``N-knights`` which will increase calculation speed drastically, as every call will be nearly instantaneous.
The On-line encylcopedia of integer sequences has these constants in a following page:
http://oeis.org/A201540.

How to install
--------------

You can install a package directly from GitHub by using this command in your terminal:

::

    python -m pip install https://

How to run
----------

The application is bundled with a ``Gunicorn`` - python WSGI HTTP Server, thus afer its installation there is
no need to install additional packages. One can run the application by invoking the following command withing the environment
where the ``phrase_chess_task`` package was installed.

::

    gunicorn --workers 4 --bind localhost:5050 --timeout 60 phrase_chess_task.api.flask_app:app

This command will spin up ``4`` processes/workers with the ``phrase_chess_task.api.flask_app:app`` Flask app that will accept clients'
requests and serve responses on `http://localhost:5050/` with a timeout for requests set for 60 seconds.

You can then test that the API works and accepts requests:

..  code-block:: shell

    curl -X POST \
    'http://localhost:5050/solve' \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "n": 5,
        "chessPiece": "queen"
    }'

For further development
=======================

Prerequisites
-------------

In case you want to contribute to the project you can clone it from this GitHub page: https://github.com/ulitival/chess_figures_placement.git.
There are prerequisites in order to be able to get this project to work. Your machine has to have installed:

- ``Poetry``: https://python-poetry.org/
- ``Pyenv``: https://github.com/pyenv/pyenv


After ``pyenv`` and ``poetry`` are successfully installed you may run `make setup` that will initiate project's setup, i.e. picking up defined in the `.python-verion` file version of python interpreter and as well set up ``poetry`` specific settings.

Initiate the project
--------------------

From within the project's root folder you may try
``poetry install`` as also defined in the Makefile as ``make init``.
That should work directly without any issues.
From that moment you can freely make changes in the code.