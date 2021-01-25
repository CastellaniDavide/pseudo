"""pseudo 
"""
from os import path
from datetime import datetime
from json import loads
import logging

__author__ = "Bellamoli Riccardo", "Castellani Davide"
__version__ = "01.01 2021-01-23"

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
		self.conf = loads(open(path.join(path.dirname(path.abspath(__file__)), "..", "conf", "pseudo.conf")).read())
		logging.info("Readed configuration file")

		first = True
		self.body = []
		body = ""
		for line in open(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", self.conf["files"]["input"])):
			line = line.strip().split(self.conf["csv_div"])
			if self.conf["header"] and first:
				first = False
				self.header = line
			else:
				body += f"{line}\n"

		self.body = self.csv2array(body[:-1:])
		logging.info("Readed input file")

	def get_positions(self):
		"""Gets the positions
		"""
		self.positions = []
		if self.conf["header"]:
			for element in self.conf["values_to_del"]:
				self.positions.append(self.header.index(element))
		else:
			self.positions = self.conf["values_to_del"]
		logging.info("Getted all position where delete")

	def elaborate_secrets(self):
		"""Clear dangerous parts and put them into self.secret_* variabile(s)
		"""
		if self.conf["header"]:
			self.secret_header = []
			for j in sorted(self.positions, reverse=True):
				self.secret_header.append(self.header[j])
				del self.header[j] 
			self.secret_header.append("ID")
			self.header.insert(0, "ID")
			self.secret_header = self.secret_header[::-1]
			logging.info("Secret header elaborated")
		
		self.secret_body = []
		mytime = int(datetime.now().timestamp())
		for index, i in enumerate(self.body):
			partial_secret = []
			for j in sorted(self.positions, reverse=True):
				partial_secret.append(i[j])
				del i[j]

			id = f"{mytime * 10000 + index}"
			partial_secret.append(id)
			self.body[index].insert(0, id)
			self.secret_body.append(partial_secret[::-1])
		logging.info("Secret body elaborated")

		logging.info("Secret elaborated")

	def write_output(self):
		"""Write my outputs
		"""
		with open(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", self.conf["files"]["output"]["public"]), "w+") as file_out:
			if self.conf["header"]: 
				file_out.write(self.array2csv([self.header,]))
			file_out.write(self.array2csv(self.body))
			
		with open(path.join(path.dirname(path.abspath(__file__)), "..", "flussi", self.conf["files"]["output"]["private"]), "w+") as file_out:
			if self.conf["header"]: 
				file_out.write(self.array2csv([self.secret_header,]))
			file_out.write(self.array2csv(self.secret_body))
		logging.info("Writed outputs")

	def csv2array(self, csv):
		""" Converts csv file to a py array
		"""
		array = []

		for line in csv.split("\n"):
			temp = []
			for item in line.replace(self.conf["csv_div"], f"'{self.conf['csv_div']}'").split(f"'{self.conf['csv_div']}'"):
				try:
					temp.append(int(item.replace('"', "")))
				except:
					temp.append(item.replace('"', ""))
			array.append(temp)

		logging.info("Converted csv into array")		
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
		try:
			if open(path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"), 'r+').read() == "":
				assert(False)
		except:
			open(path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"), 'w+').write('"message,"date-time","tick"\n')

		logging.basicConfig(filename=path.join(path.dirname(path.abspath(__file__)), "..", "log", "trace.log"), level=logging.DEBUG, format=f'"%(message)s","{datetime.now()}","{datetime.now().timestamp()}"')
		logging.info("Start")
		logging.info("Log inizialized")	
		
if __name__ == "__main__":
	pseudo()
