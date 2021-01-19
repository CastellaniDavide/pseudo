"""anonymous
"""

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2021-01-19"

class anonymous:
	def __init__ (self, div=";"):
		"""Where it all begins
		"""
		self.div = div
		self.read_input()
		self.get_positions()
		self.write_output()
	
	def read_input(self):
		"""Reads my input file(s)
		"""
		self.conf = open("../flussi/anonymus.conf").read().split("\n")

		first = True
		self.body = []

		for line in open("../flussi/example.csv"):
			line = line.strip().split(self.div)
			if first:
				first = False
				self.header = line
			else:
				self.body.append(line)

	def get_positions(self):
		"""Gets the positions
		"""
		self.positions = []
		for element in self.conf:
			self.positions.append(self.header.index(element))

	def write_output(self):
		"""Write my outputs
		"""
		file_out = open("../flussi/file_out.csv", "w+")
		for j in sorted(self.positions, reverse=True):
			del self.header[j] 
		file_out.write(f'{self.header}\n')
		for i in self.body:
			for j in sorted(self.positions, reverse=True):
				del i[j] 
			file_out.write(str(i))
			file_out.write("\n")
		file_out.close()
		
if __name__ == "__main__":
	anonymous()
