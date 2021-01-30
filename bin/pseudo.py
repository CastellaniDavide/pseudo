"""pseudo 
"""
from os import path
from datetime import datetime
from json import loads
import logging
import xml.etree.ElementTree as ET

__author__ = "Bellamoli Riccardo", "Castellani Davide"
__version__ = "02.01 2021-01-30"

class pseudo:
	def __init__ (self):
		"""Where it all begins
		"""
		self.init_log()
		self.read_input()
		self.get_positions()
		self.elaborate_secrets()
		self.write_output()

		logging.info("End")
	
	def read_input(self):
		"""Reads my input file(s)
		"""
		pseudo.printProgressBar(0, 1, suffix = 'read_input')
		self.conf = loads(open(path.join(path.dirname(path.abspath(__file__)), "..", "conf", "pseudo.conf")).read())
		logging.info("Readed configuration file")

		# Inizialize some variabiles
		self.body = []
		self.header = []
		
		# Read files
		for index, input_file in enumerate(self.conf["files"]["inputs"]):
			pseudo.printProgressBar(index + 2, len(self.conf["files"]["inputs"]) + 1, suffix = 'read_input')
			if ".csv" in input_file:
				# Elaborate csv file
				body = ""
				first = True
				for line in open(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", input_file)):
					if self.conf["header"] and first:
						first = False
						header = self.csv2array(line)[0]
						header.append("NameSheet") # TODO
					else:
						body += f"{line}\n"

				items = self.csv2array(body)
				
				# Add NameSheet
				for i in range(len(items)):
					items[i].append(input_file.replace(".csv", ""))

				self.elaborate_table(header, items)

			elif ".xml" in input_file:
				# Elaborate xml file
				root = ET.parse(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", input_file)).getroot()
				items = []
				temp = []
				self.name_sheet = []
				for elem in root.iter():
					if elem.tag == root.tag:
						continue
					if "Name" in str(elem.attrib) and "Worksheet" in str(elem):
						temp_words = str(elem.attrib).replace('{', " ").replace('}', " ").replace("'", "").replace(':', "").strip().split(" ")
						for i, word in enumerate(temp_words):
							if word == "Name":
								self.name_sheet.append(temp_words[i+1])
					if elem.text not in [None, ""]:
						if "\n" in elem.text:
							items.append(temp)
							temp = []
						else:
							temp.append(elem.text)
				temp.append(elem.text)

				# Remove extra intestations
				while [] in items : items.remove([])
				items = items[1:]
				if ['9312', '23016', '0', '0', '1', 'False', 'False'] in items : items.remove(['9312', '23016', '0', '0', '1', 'False', 'False'])

				# Add NameSheet
				j = 0
				save = True
				items2 = []
				header = None
				for i in range(len(items)):
					if 'False' in items[i]:
						save = False
						if ['False', 'False'] == items[i]:
							j += 1
					else:
						if save and items != self.header:
							items[i].append(self.name_sheet[j])
							items2.append(items[i])
						else:
							self.elaborate_table(header, items2)
							items2 = []
							header = items[i]
							save = True
				self.elaborate_table(header, items2)

		logging.info("Readed input(s) file")
		
		self.exists = {}
		self.secret_body = []
		body = ""
		first = True
		try:
			for line in open(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", self.conf["files"]["last_secret"])):
				if self.conf["header"] and first:
					first = False
				else:
					body += f"{line}\n"
			for elem in self.csv2array(body):
				self.exists[str(elem[1:])] = elem[0]
				self.secret_body.append(elem)

			logging.info("Load users IDs")
		except:
			logging.info("No user IDs to load")

	def elaborate_table(self, header, body):
		"""Elaborate a single table
		"""
		if header != None:
			# Insert new elements into the self.header
			for header_elem in header:
				if header_elem not in self.header:
					self.header.append(header_elem)

			# Get the indexes of the header
			pos_header = []
			for header_elem in header:
				pos_header.append(self.header.index(header_elem))

			# Insert new elements into the self.body
			for line in body:
				add_elem = [""] * len(self.header)
				for elem, index in zip(line, pos_header):
					add_elem[index] = elem
				self.body.append(add_elem)

	def get_positions(self):
		"""Gets the positions
		"""
		self.positions = []
		pseudo.printProgressBar(0, 1, suffix = 'get_positions')
		if self.conf["header"]:
			for i, element in enumerate(self.conf["values_to_del"]):
				self.positions.append(self.header.index(element))
				pseudo.printProgressBar(i+1, len(self.conf["values_to_del"]), suffix = 'get_positions')
		else:
			self.positions = self.conf["values_to_del"]
			pseudo.printProgressBar(1, 1, suffix = 'get_positions')
		logging.info("Getted all position where delete")

	def get_id(self, mytime, index, actual_values):
		"""Gets the ID
		"""
		if str(actual_values) in self.exists:
			return self.exists[str(actual_values)]
		else:
			id = f"{mytime * 10**6 + index}"
			self.exists[str(actual_values)] = id
			return id

	def elaborate_secrets(self):
		"""Clear dangerous parts and put them into self.secret_* variabile(s)
		"""
		pseudo.printProgressBar(0, len(self.positions) + len(self.body), suffix = 'elaborate_secrets')
		if self.conf["header"]:
			self.secret_header = []
			for i, j in enumerate(sorted(self.positions, reverse=True)):
				self.secret_header.append(self.header[j])
				del self.header[j] 
				pseudo.printProgressBar(i + 1, len(self.positions) + len(self.body), suffix = 'elaborate_secrets')
			self.secret_header.append("ID")
			self.header.insert(0, "ID")
			self.secret_header = self.secret_header[::-1]
			logging.info("Secret header elaborated")

		mytime = int(datetime.now().timestamp())
		for index, i in enumerate(self.body):
			partial_secret = []
			try:
				for j in sorted(self.positions, reverse=True):
					partial_secret.append(i[j])
					del i[j]
			except:
				pass

			if str(partial_secret[::-1]) not in self.exists:
				partial_secret.append(self.get_id(mytime, index, partial_secret[::-1]))
				self.secret_body.append(partial_secret[::-1])
			self.body[index].insert(0, self.get_id(mytime, index, partial_secret[::-1]))

			pseudo.printProgressBar(len(self.positions) + index + 1, len(self.positions) + len(self.body), suffix = 'elaborate_secrets')

		logging.info("Secret body elaborated")
		

		logging.info("Secret elaborated")

	def write_output(self):
		"""Write my outputs
		"""
		pseudo.printProgressBar(0, 2, suffix = 'write_output')
		with open(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", self.conf["files"]["output"]["public"]), "w+") as file_out:
			if self.conf["header"]: 
				file_out.write(self.array2csv([self.header,]))
			file_out.write(self.array2csv(self.body))
		pseudo.printProgressBar(1, 2, suffix = 'write_output')
		with open(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", self.conf["files"]["output"]["private"]), "w+") as file_out:
			if self.conf["header"]: 
				file_out.write(self.array2csv([self.secret_header,]))
			file_out.write(self.array2csv(self.secret_body))
		pseudo.printProgressBar(2, 2, suffix = 'write_output')
		logging.info("Writed outputs")

	def csv2array(self, csv):
		""" Converts csv file to a py array
		"""
		array = []

		for line in csv.split("\n"):
			temp = []
			temp2 = ""
			take = True
			for char in line:
				if char == self.conf['csv_div'] and take:
					temp.append(temp2)
					temp2 = ""
				elif char == '"':
					take = not take
				else:
					temp2 += char

			temp.append(temp2)
			array.append(temp)

		logging.info("Converted csv into array")
		while [""] in array : array.remove([""])
		return array

	def array2csv(self, array):
		""" Converts py array to a csv file
		"""
		text = ""

		for line in array:
			for item in line:
				text += f'"{item}"{self.conf["csv_div"]}'
			text = text[:-1:] + "\n"
		
		logging.info("Converted array into csv")
		return text
	
	def init_log(self):
		"""Inizialize the log
		"""
		pseudo.printProgressBar(0, 1, suffix = 'init_log')
		try:
			if open(path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"), 'r+').read() == "":
				assert(False)
		except:
			open(path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"), 'w+').write('"message,"date-time","tick"\n')

		logging.basicConfig(filename=path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"), level=logging.DEBUG, format=f'"%(message)s","{datetime.now()}","{datetime.now().timestamp()}"')
		open(path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"), 'a+')
		logging.info("Start")
		logging.info("Log inizialized")
		pseudo.printProgressBar(1, 1, suffix = 'init_log')
	
	def printProgressBar(iteration, total, prefix = 'Progress_pseudo:', suffix = '', decimals = 1, length = 50, fill = '#', printEnd = "\r"):
		""" Creates a progress bar
		"""
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = "\n" if iteration == total else printEnd)

if __name__ == "__main__":
	pseudo()
