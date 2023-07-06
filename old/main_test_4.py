import inspect


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
	def ciao(self):
		pass

if __name__ == "__main__":
	# Driver's code
	n = Number(2)
	n.show()

	# getmembers() returns all the
	# members of an object
	print(inspect.getmembers(n))
	for i in inspect.getmembers(n):

		# to remove private and protected
		# functions
		if not i[0].startswith('_'):

			# To remove other methods that
			# doesnot start with a underscore
			if not inspect.ismethod(i[1]):
				print(i)
