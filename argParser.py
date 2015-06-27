import sys

class argParser(object):
	def __init__(self,args={}):
		'''A simple class for parsing command line arguments.
		   args <- Dict that contains information about each argument that can be passed.
		     {[Name,isOptional]:[all Possible values,...],...}
			if all Possible values is '*', then the value is whatever is passed
		   parsed args: {Name:Value}
		'''
		self.passedArgs=sys.argv[1:]
		self.args=args
		self.parsed={}
		self.parseArgs()
	def parseArgs(self):
		for a in self.args:
			for pa in self.pasedArgs:
				if pa.startswith(a[0]):
					value = pa.split('=')
					if self.args[a][0] != '*':
						if value in self.args[a]:
							self.parsed[a[0]]=value
							break
						else:
							self.printHelp()
							sys.exit()
					self.parsed[a[0]]=value
					break
			if not a[1]:
				self.printHelp()
				sys.exit()

	def printHelp(self):
		msg=""
		for a in self.args:
			msg += ("[" if a[1] else "")
			msg += a[0] + ("]" if a[1] else "") + " - "
			if self.args[a][0] != "*":
				msg += "["
				for v in self.args[a]:
					msg += v + ", "
				msg += "]"
			else:
				msg += "[*]"
			msg += "\n"
			if len(a) > 2:
				msg += "- " + a[2] + "\n"
			msg += "\n"
		print msg

	def getArg(self,name):
		if name in self.parsed:
			return self.parsed[name]
		else:
			return None
	def getAllArgs(self):
		return self.parsed

