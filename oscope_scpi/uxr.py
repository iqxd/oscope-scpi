#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Copyright (c) 2018,2019,2020,2021, Stephen Goadhouse <sgoadhouse@virginia.edu>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#-------------------------------------------------------------------------------
#  Control of Keysight UXR series Oscilloscopes with PyVISA
#-------------------------------------------------------------------------------

# For future Python3 compatibility:
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from . import Keysight
except Exception:
    from keysight import Keysight

from time import sleep
from datetime import datetime
from quantiphy import Quantity
from sys import version_info
import pyvisa as visa

class UXR(Keysight):
    """Basic class for controlling and accessing a Keysight UXR Series Oscilloscope"""

    def __init__(self, resource, maxChannel=2, wait=0):
        """Init the class with the instruments resource string

        resource   - resource string or VISA descriptor, like TCPIP0::172.16.2.13::INSTR
        maxChannel - number of channels of this oscilloscope
        wait       - float that gives the default number of seconds to wait after sending each command
        """
        super(UXR, self).__init__(resource, maxChannel, wait)


    def measureStatistics(self):
        """Returns an array of dictionaries from the current statistics window.

        The definition of the returned dictionary can be easily gleaned
        from the code below.
        """

        statFlat = super(UXR, self)._measureStatistics()
        
        # convert the flat list into a two-dimentional matrix with seven columns per row
        statMat = [statFlat[i:i+7] for i in range(0,len(statFlat),7)]
        
        # convert each row into a dictionary, while converting text strings into numbers
        stats = []
        for stat in statMat:
            stats.append({'label':stat[0],
                          'CURR':float(stat[1]),     # Current Value
                          'MIN':float(stat[2]),      # Minimum Value
                          'MAX':float(stat[3]),      # Maximum Value
                          'MEAN':float(stat[4]),     # Average/Mean Value
                          'STDD':float(stat[5]),     # Standard Deviation
                          'COUN':int(float(stat[6])) # Count of measurements
                          })

        # return the result in an array of dictionaries
        return stats
    
    def measureDVMfreq(self, channel=None, timeout=3, wait=0.5):
        """ This is not a defined MODE for UXR series, so return string saying so
        """

        return Keysight.OverRange

    def setupAutoscale(self, channel=None):
        """ Autoscale desired channel, which is a string. channel can also be a list of multiple strings"""

        # UXR allows autoscale to either STACk, SEParate or OVERlay channels
        #
        # STACk puts them all in the same grid which reduces ADC
        # accuracy where SEParate puts them at max ADC accuracy but in
        # seperate grids.
        #@@@#self._instWrite("AUToscale:PLACement STACk")
        self._instWrite("AUToscale:PLACement SEParate")

        super(UXR, self).setupAutoscale(channel)

        
class UXRxxx4A(UXR):
    """Child class of Keysight for controlling and accessing a Keysight UXRxxx4A/UXRxxx4AP 4-Channel Oscilloscope"""

    maxChannel = 4

    def __init__(self, resource, wait=0):
        """Init the class with the instruments resource string

        resource - resource string or VISA descriptor, like TCPIP0::172.16.2.13::INSTR
        wait     - float that gives the default number of seconds to wait after sending each command
        """
        super(UXRxxx4A, self).__init__(resource, maxChannel=UXRxxx4A.maxChannel, wait=wait)

class UXRxxx2A(UXR):
    """Child class of Keysight for controlling and accessing a Keysight UXRxxx2A/UXRxxx2AP 2-Channel Oscilloscope"""

    maxChannel = 2

    def __init__(self, resource, wait=0):
        """Init the class with the instruments resource string

        resource - resource string or VISA descriptor, like TCPIP0::172.16.2.13::INSTR
        wait     - float that gives the default number of seconds to wait after sending each command
        """
        super(UXRxxx2A, self).__init__(resource, maxChannel=UXRxxx2A.maxChannel, wait=wait)

