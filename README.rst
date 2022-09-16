Timestamp maker plugin
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-timestampmaker?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-timestampmaker

.. image:: https://img.shields.io/github/license/fnndsc/pl-timestampmaker
    :target: https://github.com/FNNDSC/pl-timestampmaker/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-timestampmaker/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-timestampmaker/actions


.. contents:: Table of Contents


Abstract
--------
Create timestamps for the ChRIS project(s).


Description
-----------

``timestampmaker`` is a *ChRIS ds-type* plugin application that adds the date and time to image(s) and video(s) based on their creation time.


Usage
-----

Imaging softwares can make use of ``pl-timestampmaker`` to add or print the date and time on the image(s) and video(s) using the data that was saved along with the image(s) and video(s) when it was captured or created.


.. code::

    docker run --rm fnndsc/pl-timestampmaker timestampmaker
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        <inputDir> <outputDir>



Optional arguments
~~~~~~~~~~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.

    [--json]
    If specified, show json representation of app and exit.

    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.

    [--savejson <DIR>]
    If specified, save json representation file to DIR and exit.

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number and exit.


Getting inline help
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    docker run --rm fnndsc/pl-timestampmaker timestampmaker --man


Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-timestampmaker timestampmaker             \
        /incoming /outgoing


Development
-----------

Instructions for developers.

Building
~~~~~~~~

Build the Docker container:

.. code:: bash

    docker build -t local/pl-timestampmaker .

Local Test Run
~~~~~~~~~~~~~~

Run unit tests:

.. code:: bash

    docker run --rm local/pl-timestampmaker nosetests

Examples
--------

Put some examples here!

.. code:: bash

    docker run --rm -it                                         \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing          \
        -privileged local/pl_timestampmaker timestampmaker      \
        /incoming /outgoing



.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
