:lib:`sky130_pschulz_xx_hd` - SKY130 High Density Miscellanious Cells
=====================================================================

This library contains miscellaneous ('xx') cells for the SkyWater 130nm PDK
('sky130') optimized for high density ('hd') and provided by Paul Schulz of
MawsonLakes.Org ('pschulz').

Author: Paul Schulz <paul@mawsonlakes.org>

License: Apache License Version 2.0

Contents
--------

font-sky130
~~~~~~~~~~~

A font rendered in layer 'metal1' for adding annotations to die.

logos
~~~~~

A collection of logos rendered for use on the die produced by the SkyWater 130nm
PDK

* open-source-hardware 

Usage
-----

To use with Magic, checkout the repository and ensure that the path is in the
search path that Magic uses for cell.

Checkout::

  git clone https://github.com/PaulSchulz/sky130_pschulz_xx_hd.git

then in magic::

  addpath ./sky130_pschulz_xx_hd/mag

Alternatively, the library can be checked out into a subdirectory, eg
'libraries', in which case you want to doe something like::

  addpath ./libraries/sky130_pschulz_xx_hd/mag


