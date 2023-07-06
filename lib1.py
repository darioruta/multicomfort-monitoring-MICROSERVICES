# import json variable names under the variable de
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        #print("Input is an integer number. Number = ", val)
        return de.FORMAT_INT;
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            #print("Input is a float  number. Number = ", val)
            return de.FLOAT_FORMAT
        except ValueError:
            #print("No.. input is not a number. It's a string")
            return de.FORMAT_STRING
def check_user_input(input,supposed):
    try:
        # Convert it into integer
        val = int(input)
        #print("Input is an integer number. Number = ", val)
        return de.FORMAT_INT == supposed;
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            #print("Input is a float  number. Number = ", val)
            return de.FLOAT_FORMAT == supposed
        except ValueError:
            #print("No.. input is not a number. It's a string")
            return de.FORMAT_STRING