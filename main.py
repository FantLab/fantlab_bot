# -*- coding: utf-8 -*-

import urllib2
import telebot #pip install pytelegrambotapi
from telebot import types
from BeautifulSoup import BeautifulSoup #pip install BeautifulSoup
import random
import re
import texts
import atexit
import sys, traceback
import time
import telegram_token #файл с токеном
from bot_log import log
import bot_database as db

class Userdata:
	def __init__(self, request_step, request_string, request_data):
		self.request_step = request_step
		self.request_string = request_string
		self.request_data = request_data
		self.current_page = 1
		self.current_samepage_count = 0

users = {}

max_samepage_count = 7

def start_function(): #init database and load users
	db.init_db()
	res = db.get_alldata()
	for obj in res:
		users[obj[0]] = Userdata(obj[1], obj[2], None)

def exit_function():
	log.debug('Saving database, please wait.')
	for u in users:
		db.set_userdata(u, users[u]) #update database
	log.debug('Saved! Thank you for using this bot.')
	
start_function()
atexit.register(exit_function) # call this func on program exit
		
bot = telebot.TeleBot(telegram_token.token)

requestBasicText = 'https://fantlab.ru/bygenre?'

logicalorrequest = '&logicalor=on' # ИЛИ вместо И

def initData(chat_id):
	users[chat_id] = Userdata(0, "", None)
	random.seed()

def startFunc(message):
	messageChatId = message.chat.id
	initData(messageChatId)
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
		keyboard.add(types.InlineKeyboardButton(text = i[0], callback_data = i[1] + " " + str(i[2])))
	bot.send_message(messageChatId, texts.requestNamesArray[users[messageChatId].request_step], reply_markup = keyboard)
	users[messageChatId].request_step += 1
	
def getData(request):
	request = re.sub("\?&", "?", request)
	log.debug(request)
	soup = BeautifulSoup(urllib2.urlopen(request).read())
	table = soup.find('table')
	rows = table.findAll('tr')
	return rows

def showResult(message):
	messageChatId = message.chat.id
	if not messageChatId in users:
		users[messageChatId] = Userdata(0, "", None)
	flag = False
	if users[messageChatId].current_samepage_count == max_samepage_count:
		bot.send_message(message.chat.id, texts.pleaseWaitTheSameText)
		users[messageChatId].current_samepage_count = 0
		users[messageChatId].current_page += 1
		flag = True
	if users[messageChatId].request_data == None or flag:
		if users[messageChatId].request_string == "":
			users[messageChatId].request_string = texts.fixRequestString
		users[messageChatId].request_data = getData(requestBasicText + users[messageChatId].request_string + logicalorrequest + "&page=" + str(users[messageChatId].current_page))
	index = random.randint(3, len(users[messageChatId].request_data) - 1)
	
	cols = users[messageChatId].request_data[index].findAll('td')
	result = cols[0].getText(separator = u' ')
	result = re.sub(r"^\d+\. ", "", result)
	result = re.sub(' +',' ', result)
	
	myre = re.compile(u'(\u00AB.*\u00BB)', re.UNICODE)
	result = myre.sub(r'*\1*', result)
	
	href = cols[0].findAll('a')[0]['href']
	href = "https://fantlab.ru" + re.findall("/work.*|$", href)[0]
	result = result + "\n" + href
	log.debug(result)
	keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text = texts.iwantmoreText, callback_data = "wantanotherbook")
	button2 = types.InlineKeyboardButton(text = texts.startagainText, callback_data = "/book")
	keyboard.add(button1)
	keyboard.add(button2)
	bot.send_message(message.chat.id, result.encode('utf-8'), reply_markup = keyboard, parse_mode="Markdown")

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
		log.debug('\nFailed: ' + messageText + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		bot.send_message(messageChatId, texts.botErrorText)
		
@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			log.debug(call.message.text + " " + call.data)
			messageChatId = call.message.chat.id
			if not messageChatId in users:
				users[messageChatId] = Userdata(0, "", None)
			if call.data == '/book':
				initData(messageChatId)
				recomendationFunc(call.message)
			elif call.data == 'wantanotherbook':
				users[messageChatId].current_samepage_count += 1
				showResult(call.message)
			else:
				data = call.data.split(' ') 
				if users[messageChatId].request_step >= len(texts.requestStepsArray):
					bot.send_message(call.message.chat.id, texts.pleaseWaitText)
					showResult(call.message)
					return
				if users[messageChatId].request_step != int(data[1]) + 1:
					users[messageChatId].request_step -= 1
					recomendationFunc(call.message)
					return
				if data[0] != 'NONE': #собираем строку запроса
					users[messageChatId].request_string += data[0]
				log.debug(str(messageChatId) + " " + users[messageChatId].request_string)
				recomendationFunc(call.message)
	except Exception as e:
		log.debug('\nFailed: ' + call.data + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		bot.send_message(call.message.chat.id, texts.botErrorText)

def telegram_polling():
	try:
		bot.polling(none_stop=True, timeout = 60) #constantly get messages from Telegram
	except:
		log.error(traceback.format_exc())
		bot.stop_polling()
		time.sleep(10)
		telegram_polling()

if __name__ == '__main__':    
	telegram_polling()
