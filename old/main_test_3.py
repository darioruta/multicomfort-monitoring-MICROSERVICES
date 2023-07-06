import inspect
from datetime import datetime

from influxdb_client import InfluxDBClient,Point,WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import matplotlib.pyplot as plt
import random
import inspect

class test():
	def __init__(self):
		self.ciao = "ciao"
		self.tutto  = 4



class Number:

    # Class Attributes
    one = 'first'
    two = 'second'
    three = 'third'

    def __init__(self, attr):
        self.attr = attr

    def show(self):
        print(self.one, self.two,
              self.three, self.attr)




if __name__ == "__main__":
	t = test()
	print(f"attrib: {dir(t)}")


	# Driver's code
	n = Number(2)
	n.show()

	# getmembers() returns all the
	# members of an object
	for i in inspect.getmembers(n):

		# to remove private and protected
		# functions
		if not i[0].startswith('_'):

			# To remove other methods that
			# doesnot start with a underscore
			if not inspect.ismethod(i[1]):
				print(i)
		a=1

