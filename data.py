# -*- coding: utf-8 -*-

import telebot #pip install pytelegrambotapi
from telebot import types
import telegram_token #файл с токеном

class Userdata:
	def __init__(self, username, request_step, request_string, request_data):
		self.request_step = request_step
		self.username = username
		self.request_string = request_string
		self.request_data = request_data
		self.current_page = 1
		self.current_samepage_count = 0

users = {}
top100indexes = {}

max_samepage_count = 7

requestBasicText = 'https://fantlab.ru/bygenre?'

logicalorrequest = '&logicalor=on' # ИЛИ вместо И
allAgeRequest = "&wg106=on"

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
