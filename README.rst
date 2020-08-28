:lib:`sky130_ml_xx_hd` - SKY130 High Density Miscellanious Cells (MawsonLakes.Org Provided)
===========================================================================================

This library contains miscellaneous ('xx') cells for the SkyWater 130nm PDK
('sky130') optimized for high density ('hd') and provided by MawsonLakes.Org
('ml').

Author: Paul Schulz <paul@mawsonlakes.org>
License: Apache License Version 2.0

* font-sky130 - A font rendered in layer 'metal1' for adding annotations to die.

* logos - A collection of logos rendered for use on the die produced by the
          SkyWater 130nm PDK

To use with Magic, checkout the repository and ensure that the path is in the
search path that Magic uses for cell.

Checkout

  git clone https://github.com/PaulSchulz/sky130_ml_xx_hd.git

then in magic:

  addpath ./sky130_ml_xx_hd/mag
