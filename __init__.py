__author__ = "Devirm Celik"
__version__ = "PRE-ALPHA"

from simulation import spaceship_simulation

import logging
# write log into file only if level exceeds INFO (this is done becuase p5
# logging, which is a lot of unnecessary stuff, is from level DEBUG)
logging.basicConfig(filename='simulation.log',level=logging.INFO)
