import os

class Config():
	def __init__(self,filename):
		if not os.path.exists(filename):
			raise OSError("[ERROR] - File not found %s"%filename)

		self.filename = filename
		self.raw_data = self.readFile()
		
		returns = self.parseData()
		self.options = returns[0]
		self.errors = returns[1]

	def readFile(self):
		with open(self.filename,'r') as config:
			return config.read()

	def parseData(self):
		'''Parse the raw data from a configuration file. Grabs the variable and its subsequent value.
		returns -> [parsed,errors]
			parsed -> {variable : value, variable : value, ...}
			errors -> Integer for the amount of errors occurred

		Syntax:
			@ -> Comment
			variable=value -> Assign value to variable. Whitespace is ignored.
				Okay:
					variable = value
					    variable      =               value
				Not Okay:
					variable = 	
								value

		Supported Data Types:
			Boolean
			List
			Tuple
			String
			Integer
			Float
		'''

		returns = {}
		parsed = self.raw_data.split("\n")
		error = 0

		# Parse each line
		for line in parsed:
			# Lines starting with '@' are comments
			# Ignore whitespace
			if line.startswith("@") or line == "": continue

			else:
				try:

					var_val = line.split("=",1) # [Variable,Value]

					# Remove spaces from beginning and end
					var_val[0] = var_val[0].strip()
					var_val[1] = var_val[1].strip()

					# Value is a string
					if var_val[1].startswith('"') or var_val[1].startswith("'"):
						string = var_val[1][1:-1]

						if string.startswith("cwd\\") or string.startswith("cwd//"):
							string = os.path.join(os.path.abspath("."),string[:5])

						returns[var_val[0]] = string

					# Value is a digit
					elif var_val[1].isdigit():				returns[var_val[0]] = int(var_val[1])
					elif self.isFloat(var_val[1]):			returns[var_val[0]] = float(var_val[1])

					# Value is a list
					elif var_val[1].startswith("("):		returns[var_val[0]] = self.stringToList(var_val[1],tuple)
					elif var_val[1].startswith("["):		returns[var_val[0]] = self.stringToList(var_val[1],list)

					# Value is a boolean
					elif var_val[1].lower() == "false":		returns[var_val[0]] = False
					elif var_val[1].lower() == "true":		returns[var_val[0]] = True

					# Value is of an unknown type
					else:									returns[var_val[0]] = var_val[1]

				except Exception as e:
					print "An error has occurred while parsing %s!"%self.filename
					print type(e).__name__, str(e)

					error += 1

		return [returns,error]

	def isFloat(self,value):
		try:
			float(value)
			return True
		except ValueError:
			return False

	def stringToList(self,raw,ltype):
		contents = raw[1:-1]

		if "," in contents:
			contents = contents.split(",")

			for c in contents:
				if c.isdigit(): 								contents[contents.index(c)] = int(c)
				elif c.startswith("'") or c.startswith('"'):	contents[contents.index(c)] = c[1:-1]
				elif c.startswith("("):							contents[contents.index(c)] = self.stringToList(c,tuple)
				elif c.startswith("["):							contents[contents.index(c)] = self.stringToList(c,list)
				elif c.lower() == "false":						contents[contents.index(c)] = False
				elif c.lower() == "true": 						contents[contents.index(c)] = True
				else:											contents[contents.index(c)] = c


		return ltype(contents)

	def getOption(self,varName):
		return self.options[varName]

	def getAllOptions(self):
		return self.options
