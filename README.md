Intro
=====
This python module allows remote control of a RIGOL DM3052 digital multimeter. It bases
on work done by Matt Mets (see https://github.com/cibomahto/pyusbtmc), and was heavily extended by
Sandro Beffa

Most RIGOL devices allow remote control. This python module uses the usbtmc linux 
kernel driver to send commands to the device. See in the doc folder for the programming manual.

Install
======= 
First check if the usbtmc driver is loaded:
------------------------------------------

> lsmod | grep usbtmc.


If necessary, load the module:

> sudo modprobe usbtmc

Permissions
-----------

You need read and write access to the usbtmc device.
Check:

> ls -la /dev | grep usbtmc

If necessary, give change permissions:

> sudo chmod a+rw /dev/usbtmc0

This has to be done every time the usbtmc device is recreated (e.g. reboot, switch on/off)
The better way is to use udev for that.

Example
=======

An example for this python module can be found in the getACCurrent.py file.
This code samples the DC current.





