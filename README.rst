.. highlight:: shell

===============================
Drone dectector
===============================

.. image:: https://img.shields.io/github/v/tag/malapert/drone_dectector
.. image:: https://img.shields.io/github/v/release/malapert/drone_dectector?include_prereleases

.. image https://img.shields.io/github/downloads/malapert/drone_dectector/total
.. image https://img.shields.io/github/issues-raw/malapert/drone_dectector
.. image https://img.shields.io/github/issues-pr-raw/malapert/drone_dectector
.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/malapert/drone_dectector/graphs/commit-activity
.. image https://img.shields.io/github/license/malapert/drone_dectector
.. image https://img.shields.io/github/forks/malapert/drone_dectector?style=social


Drone detector

From sources
------------

The sources for Drone dectector can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/malapert/drone_dectector

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/malapert/drone_dectector/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ tar zxvf drone_dectector-0.1.dev0.tar.gz
    $ cd drone_dectector-0.1.dev0
    $ make  # install in the system root
    $ make user # or Install for non-root usage


.. _Github repo: https://github.com/malapert/drone_dectector
.. _tarball: https://github.com/malapert/drone_dectector/tarball/master



Development
-----------

.. code-block:: console

        $ git clone https://github.com/malapert/drone_dectector
        $ cd drone_dectector
        $ make prepare-dev
        $ source .drone_dectector
        $ make install-dev


To get more information about the preconfigured tasks:

.. code-block:: console

        $ make help

Usage
-----

To use Drone dectector in a project::

.. code-block:: console

        usage: drone_dectector [-h] [-v] [--level {INFO,DEBUG,WARNING,ERROR,CRITICAL,TRACE}] [--contour_area CONTOUR_AREA]
                            [--treshold TRESHOLD]
                            {camera,video} ...

        Drone detector

        positional arguments:
        {camera,video}

        options:
        -h, --help            show this help message and exit
        -v, --version         show program's version number and exit
        --level {INFO,DEBUG,WARNING,ERROR,CRITICAL,TRACE} set Level log (default: INFO)
        --contour_area CONTOUR_AREA set the box area from which the contour is drawn (default: 50)
        --treshold TRESHOLD   Threshold (from 0 to 255) for which we consider the images are different between the two last images (>20 /
                                255) (default: 20)


Some examples :

    * drone_dectector camera
    * drone_dectector --contour_area 80 camera
    * drone_dectector --contour_area 80 --level DEBUG camera
    * drone_dectector video --file /home/malapert/Téléchargements/test.mp4

Run tests
---------

.. code-block:: console

        $make tests



Author
------
👤 **Jean-Christophe Malapert**



🤝 Contributing
---------------
Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/malapert/drone_dectector/issues). You can also take a look at the [contributing guide](https://github.com/malapert/drone_dectector/blob/master/CONTRIBUTING.rst)


📝 License
----------
This project is [GNU General Public License v3](https://github.com/malapert/drone_dectector/blob/master/LICENSE) licensed.
