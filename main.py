# -*- coding: utf-8 -*-

import urllib2
import telebot #pip install pytelegrambotapi
from telebot import types
from BeautifulSoup import BeautifulSoup #pip install BeautifulSoup
import random
import re
import texts
import sys, traceback
import telegram_token #файл с токеном

errorfile = "Error.log"

token = telegram_token.token

bot = telebot.TeleBot(token)

requestBasicText = 'https://fantlab.ru/bygenre?'

logicalorrequest = '&logicalor=on' # ИЛИ вместо И

additionalRequestText = ""
requestStep = 0
requestData = None

def initData():
	random.seed()
	global requestStep
	global additionalRequestText
	global requestData
	requestData = None
	requestStep = 0
	additionalRequestText = ""

def startFunc(message):
	messageChatId = message.chat.id
	keyboard = types.InlineKeyboardMarkup()
	startButton = types.InlineKeyboardButton(text = texts.showRecomendsText, callback_data = "/book")
	keyboard.add(startButton)
	bot.send_message(messageChatId, texts.startText, reply_markup = keyboard)

def recomendationFunc(message):
	global requestStep
	messageChatId = message.chat.id
	keyboard = types.InlineKeyboardMarkup()
	for i in texts.requestStepsArray[requestStep]:
		keyboard.add(types.InlineKeyboardButton(text = i[0], callback_data = i[1]))
	bot.send_message(messageChatId, texts.requestNamesArray[requestStep], reply_markup = keyboard)
	requestStep += 1
	
def getData(request):
	request = re.sub("\?&", "?", request)
	print request
	soup = BeautifulSoup(urllib2.urlopen(request).read())
	table = soup.find('table')
	rows = table.findAll('tr')
	return rows
	index = random.randint(3, len(rows) - 1)
	cols = rows[index].findAll('td')
	return rows

def showResult(message):
	global requestData
	global additionalRequestText
	if requestData == None:
		if additionalRequestText == "":
			additionalRequestText = texts.fixRequestString
		requestData = getData(requestBasicText + additionalRequestText + logicalorrequest)
	index = random.randint(3, len(requestData) - 1)
	cols = requestData[index].findAll('td')
	result = cols[0].getText(separator = u' ')
	result = re.sub(r"^\d+\. ", "", result)
	result = re.sub(' +',' ', result) 
	href = cols[0].findAll('a')[0]['href']
	print href
	href = "https://fantlab.ru" + re.findall("/work.*|$", href)[0]
	result = result + "\n" + href
	print result
	keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text = texts.iwantmoreText, callback_data = "wantanotherbook")
	button2 = types.InlineKeyboardButton(text = texts.startagainText, callback_data = "/book")
	keyboard.add(button1)
	keyboard.add(button2)
	bot.send_message(message.chat.id, result.encode('utf-8'), reply_markup = keyboard)

@bot.message_handler(content_types=["text"])
def message_handler(message):
	messageChatId = message.chat.id
	messageText = message.text
	if messageText == '/start':
		startFunc(message)
	elif messageText == '/help':
		bot.send_message(messageChatId, texts.helpText)
	elif messageText == '/book':
		initData()
		recomendationFunc(message)
	else:
		startFunc(message)
		
@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == '/book':
				initData()
				recomendationFunc(call.message)
			elif call.data == 'wantanotherbook':
				showResult(call.message)
			else: 
				if requestStep >= len(texts.requestStepsArray):
					bot.send_message(call.message.chat.id, texts.pleaseWaitText)
					showResult(call.message)
					return
				global additionalRequestText
				if call.data != 'NONE': #собираем строку запроса
					additionalRequestText += call.data
				print additionalRequestText
				recomendationFunc(call.message)
	except Exception as e:
		print '\nFailed: ' + call.data
		print str(e) + "\n"
		traceback_error_string=traceback.format_exc()
		with open(errorfile, "a") as myfile:
			myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<ERROR>>\r\n"+ traceback_error_string + "\r\n<<ERROR>>")
		traceback.print_exc(file=sys.stdout)
		bot.send_message(call.message.chat.id, texts.botErrorText)

def telegram_polling(): #TODO: test!
	try:
		bot.polling(none_stop=True, timeout = 60) #constantly get messages from Telegram
	except:
		traceback_error_string=traceback.format_exc()
		with open(errorfile, "a") as myfile:
			myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<ERROR polling>>\r\n"+ traceback_error_string + "\r\n<<ERROR polling>>")
		bot.stop_polling()
		time.sleep(10)
		telegram_polling()

if __name__ == '__main__':    
	telegram_polling()
