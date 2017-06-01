# -*- coding: utf-8 -*-

import urllib2
import telebot #pip install pytelegrambotapi
from telebot import types
from BeautifulSoup import BeautifulSoup #pip install BeautifulSoup
import random
import re
import texts
import sys, traceback
import time
import sqlite3
import telegram_token #файл с токеном

dbfile = 'data.db'

class Userdata:
	def __init__(self, request_step, request_string, request_data):
		self.request_step = request_step
		self.request_string = request_string
		self.request_data = request_data

class Log:
	logfile = "log.txt"
	def __init__(self, filename):
		self.logfile = filename 

	def debug(self, string):
		print string
		with open(self.logfile, "a") as myfile:
			myfile.write(string.encode('utf8') + "\r\n")

	def error(self, string):
		print string
		with open(self.logfile, "a") as myfile:
			myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<ERROR>>\r\n"+ string.encode('utf8') + "\r\n<<ERROR>>")

log = Log("log.txt")
		
users = {}

#conn = sqlite3.connect(dbfile) #TODO: add database

token = telegram_token.token

bot = telebot.TeleBot(token)

requestBasicText = 'https://fantlab.ru/bygenre?'

logicalorrequest = '&logicalor=on' # ИЛИ вместо И

def initData(chat_id):
	users[chat_id] = Userdata(0, "", None) 
	random.seed()

def startFunc(message):
	messageChatId = message.chat.id
	users[messageChatId] = Userdata(0, "", None) #init data
	keyboard = types.InlineKeyboardMarkup()
	startButton = types.InlineKeyboardButton(text = texts.showRecomendsText, callback_data = "/book")
	keyboard.add(startButton)
	bot.send_message(messageChatId, texts.startText, reply_markup = keyboard)

def recomendationFunc(message):
	messageChatId = message.chat.id
	if not messageChatId in users:
		users[messageChatId] = Userdata(0, "", None) 
	keyboard = types.InlineKeyboardMarkup()
	for i in texts.requestStepsArray[users[messageChatId].request_step]:
		keyboard.add(types.InlineKeyboardButton(text = i[0], callback_data = i[1]))
	bot.send_message(messageChatId, texts.requestNamesArray[users[messageChatId].request_step], reply_markup = keyboard)
	users[messageChatId].request_step += 1
	
def getData(request):
	request = re.sub("\?&", "?", request)
	log.debug(request)
	soup = BeautifulSoup(urllib2.urlopen(request).read())
	table = soup.find('table')
	rows = table.findAll('tr')
	return rows
	index = random.randint(3, len(rows) - 1)
	cols = rows[index].findAll('td')
	return rows

def showResult(message):
	messageChatId = message.chat.id
	if not messageChatId in users:
		users[messageChatId] = Userdata(0, "", None) 
	if users[messageChatId].request_data == None:
		if users[messageChatId].request_string == "":
			users[messageChatId].request_string = texts.fixRequestString
		users[messageChatId].request_data = getData(requestBasicText + users[messageChatId].request_string + logicalorrequest)
	index = random.randint(3, len(users[messageChatId].request_data) - 1)
	cols = users[messageChatId].request_data[index].findAll('td')
	result = cols[0].getText(separator = u' ')
	result = re.sub(r"^\d+\. ", "", result)
	result = re.sub(' +',' ', result) 
	href = cols[0].findAll('a')[0]['href']
	href = "https://fantlab.ru" + re.findall("/work.*|$", href)[0]
	result = result + "\n" + href
	log.debug(result)
	keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text = texts.iwantmoreText, callback_data = "wantanotherbook")
	button2 = types.InlineKeyboardButton(text = texts.startagainText, callback_data = "/book")
	keyboard.add(button1)
	keyboard.add(button2)
	bot.send_message(message.chat.id, result.encode('utf-8'), reply_markup = keyboard)

@bot.message_handler(content_types=["text"])
def message_handler(message):
	try: 
		messageChatId = message.chat.id
		messageText = message.text
		log.debug(messageText)
		if messageText == '/start':
			startFunc(message)
		elif messageText == '/help':
			bot.send_message(messageChatId, texts.helpText)
		elif messageText == '/book':
			initData(messageChatId)
			recomendationFunc(message)
		else:
			startFunc(message)
	except Exception as e:
		log.debug('\nFailed: ' + call.data + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		bot.send_message(call.message.chat.id, texts.botErrorText)
		
@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			log.debug(call.message.text + " " + call.data)
			messageChatId = call.message.chat.id
			if call.data == '/book':
				initData(messageChatId)
				recomendationFunc(call.message)
			elif call.data == 'wantanotherbook':
				showResult(call.message)
			else:
				if not messageChatId in users:
					users[messageChatId] = Userdata(0, "", None) 
				if users[messageChatId].request_step >= len(texts.requestStepsArray):
					bot.send_message(call.message.chat.id, texts.pleaseWaitText)
					showResult(call.message)
					return
				if call.data != 'NONE': #собираем строку запроса
					users[messageChatId].request_string += call.data
				log.debug(str(messageChatId) + " " + users[messageChatId].request_string)
				recomendationFunc(call.message)
	except Exception as e:
		log.debug('\nFailed: ' + call.data + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		bot.send_message(call.message.chat.id, texts.botErrorText)

def telegram_polling(): #TODO: test!
	try:
		bot.polling(none_stop=True, timeout = 60) #constantly get messages from Telegram
	except:
		log.error(traceback.format_exc())
		bot.stop_polling()
		time.sleep(10)
		telegram_polling()

if __name__ == '__main__':    
	telegram_polling()
