# os-sem1/__init__.py

from .pagereplacement import fifo_replacement, lru_replacement, optimal_replacement

from .diskfcfs import diskfcfs
from .disksstf import disksstf
from .diskscan import diskscan
from .diskcscan import diskcscan

from .cpufcfs import cpufcfs
from .cpusrtf import cpusrtf
from .cpusjf import cpusjf
from .cpuroundrobin import cpuroundrobin
from .cpunonpreemptive import cpunonpreemptive
from .cpupreemptive import cpupreemptive