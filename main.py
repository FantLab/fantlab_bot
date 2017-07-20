# -*- coding: utf-8 -*-

import urllib2
import telebot #pip install pytelegrambotapi
from telebot import types
from BeautifulSoup import BeautifulSoup #pip install BeautifulSoup
import random
import re
import atexit
import sys, traceback
import time
import requests
import threading
from threading import Thread

import telegram_token #файл с токеном
import texts
from texts import top100questions
from bot_log import log
import bot_database as db

#TODO list:
	#Добиться стабильности работы
	#перенести часть функций из main.py в отдельные файлы
	#Было бы неплохо, если вопросы менялись - можно спрашивать: "вам для детей или что-нибудь посерьезнее"
	#выдача книг только с высокой оценкой, минимальная оценка регулируется пользователем;
	#оценка книг (+/-) и сокрытие их из выдачи;
	#поиск по авторам с выдачей биографий;
	#поиск по названию книги;
	#более точный жанровый поиск, аналогичный полной версии на сайте;
	#связь с автором и отправка замечаний и предложений непосредственно самому боту.

def thread_save_database():
	while True:
		save_database()
		time.sleep(300)

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

def top100ArrayToString(index1, index2, array):
	if len(array) == 2:
		return str(array[1])
	else:
		return str(index1) + "\n" + str(index2)

def top100Func(message):
	messageChatId = message.chat.id
	if not messageChatId in users:
		users[messageChatId] = Userdata(getUsername(message.chat), 0, "", None) 
	keyboard = types.InlineKeyboardMarkup()
	localindex = top100indexes[messageChatId] - 1
	k = 0
	for i in top100questions[localindex][2]:
		keyboard.add(types.InlineKeyboardButton(text = i[0], callback_data = "top100_goto\n" + top100ArrayToString(localindex, k, i)))
		k += 1
	keyboard.add(types.InlineKeyboardButton(text = texts.goback, callback_data = "top100_goback " + str(top100questions[localindex][1])))
	bot.send_message(messageChatId, top100questions[localindex][0], reply_markup = keyboard)
	
def top100Result(messageChatId, index1, index2):
	array = top100questions[index1][2][index2]
	result = array[3] + " *" + array[2] + "*\nhttps://fantlab.ru/work" + array[1]
	top100Button = types.InlineKeyboardButton(text = texts.showtop100AgainText, callback_data = "/top100")
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(top100Button)
	
	bot.send_message(messageChatId, result, reply_markup = keyboard, parse_mode="Markdown")

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

def start_function(): #init database and load users
	db.init_db()
	res = db.get_alldata()
	for obj in res:
		users[obj[0]] = Userdata(obj[3], obj[1], obj[2], None)
		
def save_database():
	log.debug('Saving database, please wait.')
	for u in users:
		db.set_userdata(u, users[u]) #update database
	log.debug('Saved!')

def exit_function():
	save_database()
	log.debug('Thank you for using this bot. Bye!\n')
	
start_function()
atexit.register(exit_function) # call this func on program exit
		
bot = telebot.TeleBot(telegram_token.token)

requestBasicText = 'https://fantlab.ru/bygenre?'

logicalorrequest = '&logicalor=on' # ИЛИ вместо И
allAgeRequest = "&wg106=on"

def initData(chat):
	users[chat.id] = Userdata(getUsername(chat), 0, "", None)
	top100indexes[chat.id] = 1
	random.seed()

def startFunc(message):
	messageChatId = message.chat.id
	initData(message.chat)
	keyboard = types.InlineKeyboardMarkup()
	startButton = types.InlineKeyboardButton(text = texts.showRecomendsText, callback_data = "/book")
	top100Button = types.InlineKeyboardButton(text = texts.showtop100Text, callback_data = "/top100")
	keyboard.add(startButton)
	keyboard.add(top100Button)
	bot.send_message(messageChatId, texts.startText, reply_markup = keyboard)

def recomendationFunc(message):
	messageChatId = message.chat.id
	if not messageChatId in users:
		users[messageChatId] = Userdata(getUsername(message.chat), 0, "", None) 
	keyboard = types.InlineKeyboardMarkup()
	for i in texts.requestStepsArray[users[messageChatId].request_step]:
		keyboard.add(types.InlineKeyboardButton(text = i[0], callback_data = i[1] + " " + str(i[2])))
	bot.send_message(messageChatId, texts.requestNamesArray[users[messageChatId].request_step], reply_markup = keyboard)
	users[messageChatId].request_step += 1
	
def getData(request):
	request = re.sub("\?&", "?", request)
	log.debug("Request = " + request)
	soup = BeautifulSoup(urllib2.urlopen(request).read())
	table = soup.find('table')
	if table is None:
		request += allAgeRequest #add extra request to avoid none data
		soup = BeautifulSoup(urllib2.urlopen(request).read())
		table = soup.find('table')
	rows = table.findAll('tr')
	return rows

def showResult(message):
	messageChatId = message.chat.id
	if not messageChatId in users:
		users[messageChatId] = Userdata(getUsername(message.chat), 0, "", None)
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
	index = random.randint(3, len(users[messageChatId].request_data) - 2)
	
	cols = users[messageChatId].request_data[index].findAll('td')
	result = cols[0].getText(separator = u' ')
	result = re.sub(r"^\d+\. ", "", result)
	result = re.sub(' +',' ', result)
	
	myre = re.compile(u'(\u00AB.*\u00BB)', re.UNICODE)
	result = myre.sub(r'*\1*', result)
	
	href = cols[0].findAll('a')[0]['href']
	href = "https://fantlab.ru" + re.findall("/work.*|$", href)[0]
	result = result + "\n" + href
	log.debug("Result = " + result)
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
		log.debug("Message = " + str(messageChatId) + " " + messageText)
		if messageText == '/start':
			startFunc(message)
		elif messageText == '/help':
			bot.send_message(messageChatId, texts.helpText)
		elif messageText == '/book':
			initData(message.chat)
			recomendationFunc(message)
		elif messageText == '/top100':
			initData(message.chat)
			top100Func(message)
		else:
			startFunc(message)
	except Exception as e:
		#TODO: forward messages when error happens: bot.forward_message(id, messageChatId, message.message_id)
		log.debug('\nFailed: ' + messageText + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		bot.send_message(messageChatId, texts.botErrorText)
		
@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			log.debug("Callback = " + call.message.text + " " + call.data)
			messageChatId = call.message.chat.id
			if not messageChatId in users:
				users[messageChatId] = Userdata(getUsername(call.message.chat), 0, "", None)
			if call.data == '/book':
				initData(call.message.chat)
				recomendationFunc(call.message)
			elif call.data == 'wantanotherbook':
				users[messageChatId].current_samepage_count += 1
				showResult(call.message)
			elif call.data == '/top100':
				initData(call.message.chat)
				top100Func(call.message)
			elif call.data.find("top100_goto") >= 0:
				data = call.data.split('\n')
				if len(data) == 2:
					top100indexes[messageChatId] = int(data[1])
					top100Func(call.message)
				else:
					top100Result(messageChatId, int(data[1]), int(data[2]))
			elif call.data.find("top100_goback") >= 0:
				data = call.data.split(' ')
				if data[1] == '0':
					top100indexes[messageChatId] = int(data[1])
					startFunc(call.message)
				else:
					top100indexes[messageChatId] = int(data[1])
					top100Func(call.message)
			else:
				data = call.data.split(' ')
				if users[messageChatId].request_step != int(data[1]) + 1:
					users[messageChatId].request_step -= 1
					recomendationFunc(call.message)
					return
				if data[0] != 'NONE': #собираем строку запроса
					users[messageChatId].request_string += data[0]
				log.debug("Request string = " + str(messageChatId) + " " + users[messageChatId].request_string)
				if users[messageChatId].request_step >= len(texts.requestStepsArray):
					bot.send_message(call.message.chat.id, texts.pleaseWaitText)
					showResult(call.message)
					return
				recomendationFunc(call.message)
	except Exception as e:
		log.debug('\nFailed: ' + call.data + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		bot.send_message(call.message.chat.id, texts.botErrorText)

def telegram_polling():
	while True:
		try:
			bot.polling(none_stop=True, timeout = 60) #constantly get messages from Telegram
			sys.exit() #ha-ha
		except SystemExit: #handle sys.exit()
			sys.exit()
		except requests.exceptions.ConnectionError:
			save_database()
			log.error("Network problem")
			time.sleep(300)
		except:
			log.error(traceback.format_exc())
			bot.stop_polling()
			time.sleep(60)

if __name__ == '__main__':
	t = threading.Thread(target = thread_save_database)
	t.daemon = True #to kill this thread when main thread is killed
	t.start()
	telegram_polling()
