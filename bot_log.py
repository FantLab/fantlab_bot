# -*- coding: utf-8 -*-

import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Log:
	logfile = "log.txt"
	def __init__(self, filename):
		self.logfile = filename

	def debug(self, string):
		print string
		with open(self.logfile, "a") as myfile:
			myfile.write(time.strftime("%c") + ": " + string.encode('utf8') + "\r\n")

	def error(self, string):
		print string
		with open(self.logfile, "a") as myfile:
			myfile.write("\r\n" + time.strftime("%c")+"\r\n<<ERROR>>\r\n"+ string.encode('utf8') + "\r\n<<ERROR>>\r\n")

log = Log("log.txt")
