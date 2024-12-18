======
pyEGAF
======

This project is a Python package enabling interaction, manipulation, and analysis of thermal-neutron capture gamma-ray data from the Evaluated Gamma-ray Activation File (EGAF) library [FIR2007]_, [REV2004]_.  The EGAF library is a database of :math:`\gamma`-ray energies and their corresponding partial :math:`\gamma`-ray cross sections from thermal-neutron capture measurements carried out with a guided neutron beam at the Budapest Research Reactor for 245 isotopes encompassing measurements of natural elemental samples for targets from *Z* = 1-83, 90, and 92, except for Tc (*Z* = 43) and Pm (*Z* = 61).  The database comprises a total of 8172 primary :math:`\gamma` rays and 29605 secondary :math:`\gamma` rays (a total of 37777 :math:`\gamma` rays) associated with 12564 levels.  The (*n*, :math:`\gamma`) targets and corresponding residual compound nuclides relevant to the EGAF project are summarized in the schematic of the nuclear chart shown in the figure below.


.. image:: https://github.com/AaronMHurst/python_egaf/blob/main/EGAF_nuclides.png?raw=true
   :width: 500 px
   :scale: 100%
   :alt: Schematic of nuclear chart relevant to EGAF nuclides
   :align: center

The `pyEGAF` package provides users with a convenient means of access and visualization of the thermal neutron-capture data in EGAF including decay-scheme information and associated nuclear structure properties for all compound nuclides contained therein.  In addition, the package also provides a capability to search by :math:`\gamma`-ray energy for forensics applications.

-------------------------
Building and installation
-------------------------

The project can be built and installed conveniently using the `pip` command in a Unix terminal:

.. code:: bash

   $ pip install pyEGAF

Althernatively, because this project is also maintained on `GitHub <https://github.com/AaronMHurst/python_egaf>`_, it can be installed by cloning the repository and executing the installation script provided as described in the `README.md` documentation:

`<https://github.com/AaronMHurst/python_egaf>`_

A suite of Python modules comprising 224 unit tests is also bundled with the software.  Instructions for running the test script are also provided on `GitHub <https://github.com/AaronMHurst/python_egaf>`_.


--------------
Running pyEGAF
--------------

Following installation, the `pyEGAF` scripts can be ran from any location by importing the package and making an instance of the `EGAF` class:

.. code-block:: bash
		
	$ python


.. code-block:: python
	
	import pyEGAF as egaf
	e = egaf.EGAF()


Most methods also require passing the EGAF `JSON` source data set as a list-object argument which first needs to be created:

.. code-block:: python

	edata = e.load_egaf()


The utility of the `pyEGAF` methods illustrating examples concerning access, manipulation, analysis, and visualization of the EGAF data is demonstrated in the `Jupyter Notebooks` provided on `GitHub <https://github.com/AaronMHurst/python_egaf>`_.  These notebooks also have a `matplotlib` Python-package dependency and utilize inline-plotting methods and builtin `Jupyter Notebook` magic commands.  

----------
Docstrings
----------

All `pyEGAF` classes and functions have supporting docstrings.  Please refer to the individual dosctrings for more information on any particular function including how to use it.  The dosctrings for each method generally have the following structure:

* A short explanation of the function.
* A list and description of arguments that need to be passed to the function.
* The return value of the function.
* An example(s) invoking use of the function.

---------------------
EGAF source data sets
---------------------

Although the `pyEGAF` methods already provide greatly enhanced user access to the EGAF data, the original data sets are also bundled with this software package for convenience and to allow users to curate data in a bespoke manner should they prefer.  The data sets are provided in the following three formats:

* Evaluated Nuclear Structure Data File (ENSDF);
* Reference Input Parameter Library (RIPL);
* JavaScript Object Notation (JSON).

Each of these formats are described briefly below.

------------
ENSDF format
------------

The original EGAF data sets were prepared in accordance with the mixed-record 80-character column format of the Evaluated Nuclear Structure Data File (ENSDF) [TUL2001]_.  These ENSDF-formatted files are maintained online by the International Atomic Energy Agency [EGAIAEA]_.  The relevant fields of the `Normalization`, `Level`, and `Gamma` records that are commonly adopted in the EGAF data sets are explained in the ENSDF manual [TUL2001]_.  In addition, `Comment` records are also frequently encountered in EGAF data sets.  The ENSDF-formatted EGAF data sets can be accessed using `pyEGAF` methods by passing the EGAF data set list object and the *residual compound nucleus* produced in an (*n*, :math:`\gamma`) reaction, for example, \ :sup:`28` Si(*n*, :math:`\gamma`)\ :sup:`29` Si:

.. code-block:: python
		
   ensdf = e.get_ensdf(edata, "Si29")


File printing is suppressed by default.  To print the file to your `pwd` pass the boolean argument `True` to the same function:

.. code-block:: python

   ensdf = e.get_ensdf(edata, "Si29", True)


This will create the file `EGAF_ENSDF_28SI_NG_29SI.ens` in the current working directory.


-----------
RIPL format
-----------

Because many nuclear reaction codes source decay-scheme information in a particular Reference Input Parameter Library (RIPL) [CAP2008]_ format, representative RIPL-translated data sets have also been generated for each corresponding EGAF data set and are bundled with the software.  The RIPL-formatted EGAF data sets can also be accessed from the interpreter, for example, \ :sup:`28` Si(*n*, :math:`\gamma`)\ :sup:`29` Si:

.. code-block:: python
		
   ripl = e.get_ripl(edata, "Si29") # Or,
   ripl = e.get_ripl(edata, "Si29", True) # To print the file in the pwd

Passing `True` to the callable will print-to-file the RIPL-formatted decay scheme information as `EGAF_RIPL_Si28_NG_Si29.dat` in the current working directory.  The proton- and neutron-separation energies in the RIPL headers are taken from the 2020 Atomic Mass Evaluation [WAN2020]_.

-----------
JSON format
-----------

All original EGAF data sets have been translated into a representative JavaScript Object Notation (JSON) format using an intuitive syntax to describe the quantities sourced from the primary and continuation records [TUL2001] of the ENSDF-formatted data sets.  The JSON-formatted data sets are also bundled with the software package and can again be accessed through the interpreter, for example, \ :sup:`28` Si(*n*, :math:`\gamma`)\ :sup:`29` Si:

.. code-block:: python
		
   jfile = e.get_json(edata, "Si29") # Or,
   jfile = e.get_json(edata, "Si29", True) # To print the file in the pwd

Passing `True` to the callable will print-to-file the corresponding JSON data structure as `EGAF_JSON_Si28_NG_Si29.json` in the current working directory.

The JSON data structures support the following data types:

* *string*
* *number*
* *boolean*
* *null*
* *object* (JSON object)
* *array*

The JSON-formatted EGAF schema is explained in detail in the `README.md` on `GitHub <https://github.com/AaronMHurst/python_egaf>`_.


----------
References
----------

.. [FIR2007]
   R.B.Firestone *et al*., *"Database of Prompt Gamma Rays from Slow Thermal Neutron Capture for Elemental Analysis"*, IAEA STI/PUB/1263, 251 (2007); https://www-nds.iaea.org/pgaa/egaf.html

   
.. [REV2004]
   Z.Revay, R.B. Firestone, T. Belgya, G.L. Molnar, *"Handbook of Prompt Gamma Activation Analysis"*, edited by G.L. Molnar (Kluwer Academic Dordrecht, 2004), Chap. Prompt Gamma-Ray Spectrum Catalog, p. 173.


.. [TUL2001]
   J.K.Tuli, *"Evaluated Nuclear Structure Data File"*, BNL-NCS-51655-01/02-Rev (2001).


.. [EGAIAEA]
   Evaluated Gamma-ray Activation File (EGAF); https://www-nds.iaea.org/pgaa/egaf.html


.. [CAP2008]
   R.Capote *et al*., *"RIPL - Reference Input Parameter Library for Calculation of Nuclear Reactions and Nuclear Data Evaluations"*, Nucl. Data Sheets **110**, 3107 (2009).

.. [WAN2020]
   M.Wang, W.J. Huang, F.G. Kondev, G. Audi, S. Naimi, *"The AME2020 atomic mass evaluation"*, Chin. Phys. C **45**, 030003 (2021).
   
