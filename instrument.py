"""This module gives access to some basic functions provided by a RIGOL DM3052 digital
   multi meter. To communicate with the device, the usbmtc kernel driver is used.
   The protocol to communicate with the device is ASCII based, the documentation can be found 
   in the doc folder"""

import os
import time
import sys

class usbtmc:
    """Simple implementation of a USBTMC device driver, in the style of visa.h"""

    def __init__(self, device):
        self.device = device
       
	try:
		self.FILE = os.open(device, os.O_RDWR)
	
	except OSError as e:
		print e	
		
		print "Have you loaded the usbtmc kernel driver?"
		print "Check with: lsmod | grep usbtmc"

		print "If yes, check permissions of the device file:"
		print "ls -la /dev | grep usbtmc"
		print "You should have write and read access:"
		print "sudo chmod a+rw /dev/usbtmc0"

		print "If not, load the module with:"
		print "sudo modprobe usbtmc"

		sys.exit(0)

	except Exception as e:
       		print("oops..an error happend: follwing exception was thrown:")
		print type(e)
		sys.exit(0)


    def write(self, command):
        os.write(self.FILE, command);

    def read(self, length = 4000):
        return os.read(self.FILE, length)

    def getName(self):
        self.write("*IDN?")
        return self.read(300)

    def sendReset(self):
        self.write("*RST")


class RigolScope:
    """Class to control a Rigol DS1000 series oscilloscope"""
    def __init__(self, device):
        self.meas = usbtmc(device)

        self.name = self.meas.getName()

        print self.name

    def write(self, command):
        """Send an arbitrary command directly to the scope"""
        self.meas.write(command)

    def read(self, command):
        """Read an arbitrary amount of data directly from the scope"""
        return self.meas.read(command)

    def reset(self):
        """Reset the instrument"""
        self.meas.sendReset()


class RigolDM3000(RigolScope):
	"""Class to control a Rigol DM3052 digital multimeter"""

	numberOfSamples=300
	sampleTime = 0	
	

	def setNumberOfSamples(self, samples):
		self.numberOfSamples = samples
		#sample time in mili seconds
                self.sampleTime = (self.numberOfSamples / 100)*1000		

	def __init__(self, device):
		RigolScope.__init__(self, device)
		
		#sample time in mili seconds
		self.sampleTime = (self.numberOfSamples / 100)*1000


	def datalog(self):

        	self.write(":DATAlog:CONFigure:FUNCtion DCI,2")
        	self.write(":DATAlog:CONFigure:STARtmode:AUTO")
        	self.write(":DATAlog:CONFigure:STOPmode:NUMber %s" % self.numberOfSamples)
        	self.write(":DATAlog:CONFigure:RATE 8")
        	self.write(":DATAlog:RUN")

        	self.write(":DATAlog:RUN?")   
        	status = self.read(20)

        	while(status.rstrip() != "STOP"):
                	time.sleep(0.5)
                	self.write(":DATAlog:RUN?")   
                	status = self.read(20)
 
		
		steps = self.sampleTime / self.numberOfSamples
		data_time = range(steps,self.sampleTime+steps,steps)

		data = self.getData()

		if(len(data_time) != len(data)):
			print("number of y-elements: %s " % len(data_time))
			print("number of x-elements: %s " % len(data))

			raise ValueError("time and data arrangement does not match!")		

		else:
        		return {"data": data, "time": data_time} 

	def getData(self):


		processedSamples = self.numberOfSamples
	
		data = []	

		while(processedSamples > 0):

			self.write(":DATAlog:DATA? 1,100")

        		#get the data
        		chunk = self.read(9000)
       
	   		chunk.rstrip()
        		
			rawdata = chunk.split(',')

			for c in rawdata:
				data.append(c.rstrip())
			
			processedSamples = processedSamples - 100

        	l=[]
        	for i in data:

                	try:
                        	l.append(float(i.rstrip()))

                	except ValueError:

                        	print("found bad value...")
		
		return l

	def singleMeasure(self):
        	self.write(":FUNCtion:CURRent:DC")
        	self.write(":RESOlution:CURRent:DC 2")
        	self.write(":MEASure:CURRent:DC 2")

        	count = 10

       		while(count > 0):

                	self.write(":MEASure:CURRent:DC?")
                	print(self.read(20))
                	count=count -1


