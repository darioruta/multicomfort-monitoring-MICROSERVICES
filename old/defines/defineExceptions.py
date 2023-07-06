
class Exception():
	def __init__(self):
		self.DONE_CORRECT = 0
		self.EXCEPTION_UPDATING_FAILED = 1
		self.EXCEPTION_OBJECT_NOT_PRESENT = 2
		self.EXCEPTION_DELETE_FAILED = 6
		self.EXCEPTION_READ_FAILED = 3
		self.EXCEPTION_ADD_OBJECT_FAILED = 4
		self.EXCEPTION_PARAMS_CATALOG_NOT_VALID = 5
	#def SetException(self, err):
	#	self.oc.PrintErrorMessage(err)
	#	return err
