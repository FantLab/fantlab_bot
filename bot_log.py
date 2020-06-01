# -*- coding: utf-8 -*-

import time

class Log:
	logfile = "log.txt"
	def __init__(self, filename):
		self.logfile = filename

	def debug(self, string):
		print(string)
		with open(self.logfile, "a") as logfile:
			logfile.write(time.strftime("%c") + ": " + string + "\n")

	def error(self, string):
		print(string)
		with open(self.logfile, "a") as logfile:
			logfile.write(time.strftime("%c")+"<<ERROR>>"+ string + "<<ERROR>>\n")

log = Log("log.txt")
