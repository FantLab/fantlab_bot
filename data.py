# -*- coding: utf-8 -*-

import time
import telebot #pip install pytelegrambotapi
import telegram_token #файл с токеном
from bot_log import log

class Userdata:
	def __init__(self, username, request_step, request_string, request_data):
		self.request_step = request_step
		self.username = username
		self.request_string = request_string
		self.request_data = request_data
		self.current_page = 1
		self.current_samepage_count = 0
		
class Answer:
	def __init__(self, answer, count, date):
		self.answer = answer
		self.count = count
		self.date = date
		
class Version:
	def __init__(self, main, major, minor):
		self.main = main
		self.major = major
		self.minor = minor
		
VERSION = Version(1, 0, 0)

users = {}
answers = {}
top100indexes = {}

max_samepage_count = 7

requestBasicText = 'https://fantlab.ru/bygenre?'

logicalorrequest = '&logicalor=on' # ИЛИ вместо И
allAgeRequest = "&wg106=on"

WARNING_COUNT = 3
ERROR_COUNT = 5
TIME_DIFF = 3

bot = telebot.TeleBot(telegram_token.token)

def getUsername(chat):
	result = ''
	if chat.first_name:
		result += chat.first_name + ' '
	if chat.last_name:
		result += chat.last_name + ' '
	if chat.username:
		if len(result) > 0:
			result += "(" + chat.username + ")"
		else:
			result = chat.username
	return result

def botSendMessage(id, text, **kwargs):
	if not id in answers or answers[id].answer != text:
		answers[id] = Answer(text, 1, int(time.time()))
	if answers[id].count >= WARNING_COUNT and time.time() - answers[id].date <= TIME_DIFF:
		return
	if answers[id].count >= ERROR_COUNT: #TODO: goto start function or just call some telebot function to clear requests
		return
	answers[id].count += 1
	bot.send_message(id, text, **kwargs)

