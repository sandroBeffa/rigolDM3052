#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import instrument
from pylab import *


# Initialize
dm = instrument.RigolDM3000("/dev/usbtmc0")
util = instrument.Utility()

dm.setNumberOfSamples(600)
dm.setSamplingMethod("DCI")

 
log = dm.datalog()
util.saveLogToFile(log, "log.txt")



fig = figure(1, figsize=(20,5))

majorLocator   = MultipleLocator(500)
ax = subplot(111)

plt.plot(log['time'], log['data'])

ax.xaxis.set_major_locator(majorLocator)

plt.show()
