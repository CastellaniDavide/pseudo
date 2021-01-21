"""anonymous
"""

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2021-01-19"

class anonymous:
	def __init__ (self, div=","):
		"""Where it all begins
		"""
		self.div = div
		self.read_input()
		self.get_positions()
		self.elaborate_secrets()
		self.write_output()
	
	def read_input(self):
		"""Reads my input file(s)
		"""
		self.conf = open("../flussi/anonymus.conf").read().split("\n")
		while "" in self.conf: self.conf.remove("")

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

	def elaborate_secrets(self):
		"""Clear dangerous parts and put them into self.secret_* variabile(s)
		"""
		self.secret_header = []
		for j in sorted(self.positions, reverse=True):
			self.secret_header.append(self.header[j])
			del self.header[j] 
		self.secret_header = self.secret_header[::-1]
		
		self.secret_body = []
		for i in self.body:
			partial_secret = []
			for j in sorted(self.positions, reverse=True):
				partial_secret.append(i[j])
				del i[j]
			self.secret_body.append(partial_secret[::-1])

	def write_output(self):
		"""Write my outputs
		"""		
		with open("../flussi/file_out.csv", "w+") as file_out:
			file_out.write(self.array2csv([self.header,]))
			file_out.write(self.array2csv(self.body))

		with open("../flussi/file_out_secret.csv", "w+") as file_out:
			file_out.write(self.array2csv([self.secret_header,]))
			file_out.write(self.array2csv(self.secret_body))

	def csv2array(self, csv):
		""" Converts csv file to a py array
		"""
		array = []

		for line in csv.split("\n"):
			temp = []
			for item in line.replace(self.div, f"'{self.div}'").split(f"'{self.div}'"):
				try:
					temp.append(int(item.replace('"', "")))
				except:
					temp.append(item.replace('"', ""))
			array.append(temp)

		return array

	def array2csv(self, array):
		""" Converts py array to a csv file
		"""
		text = ""

		for line in array:
			for item in line:
				text += f'"{item}"{self.div}'
			text = text[:-1:] + "\n"

		return text
		
if __name__ == "__main__":
	anonymous()
