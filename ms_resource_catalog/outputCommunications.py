
import defines.defineExceptions as deExcept
ex = deExcept.Exception()

class outputCommunications():
	def __init__(self):
		pass
	def PrintErrorMessage(self, err_code):
		if err_code == ex.EXCEPTION_UPDATING_FAILED:
			print("ERROR UPDATING JSON FILE")
		elif err_code == ex.EXCEPTION_DELETE_FAILED:
			print("EXCEPTION_DELETE_FAILED")
		elif err_code == ex.EXCEPTION_OBJECT_NOT_PRESENT:
			print("EXCEPTION_OBJECT_NOT_PRESENT")
		else:
			print("PIPPO")
		