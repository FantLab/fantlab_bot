# -*- coding: utf-8 -*-

import atexit
import sys
import traceback
import time
import threading
import requests

from data import bot, Userdata, users, getUsername, top100indexes
from recommendation import initData, startFunc, recomendationFunc, showResult
from top100 import top100Func, top100Result
import texts
from bot_log import log
import bot_database as db

#TODO list:
	#Добиться стабильности работы
	#Неплохо, если бы вопросы менялись - можно спрашивать: "вам для детей или что-нибудь посерьезнее"
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

def start_function(): #init database and load users
	db.init_db()
	res = db.get_alldata()
	for obj in res:
		users[obj[0]] = Userdata(obj[3], obj[1], obj[2], None)

def save_database():
	log.debug('Saving database, please wait.')
	for user in users:
		db.set_userdata(user, users[user]) #update database
	log.debug('Saved!')

def exit_function():
	save_database()
	log.debug('Thank you for using this bot. Bye!\n')

start_function()
atexit.register(exit_function) # call this func on program exit

@bot.message_handler(content_types=["text"])
def message_handler(message):
	try:
		message_chat_id = message.chat.id
		message_text = message.text
		log.debug("Message = " + str(message_chat_id) + " " + message_text)
		if message_text == '/start':
			startFunc(message)
		elif message_text == '/help':
			bot.send_message(message_chat_id, texts.helpText)
		elif message_text == '/book':
			initData(message.chat)
			recomendationFunc(message)
		elif message_text == '/top100':
			initData(message.chat)
			top100Func(message)
		else:
			startFunc(message)
	except Exception as e:
		#TODO: forward messages when error happens: bot.forward_message(id, messageChatId, message.message_id)
		log.debug('\nFailed: ' + message_text + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		bot.send_message(message_text, texts.botErrorText)

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
			bot.polling(none_stop=True, timeout=60) #constantly get messages from Telegram
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
	t = threading.Thread(target=thread_save_database)
	t.daemon = True #to kill this thread when main thread is killed
	t.start()
	telegram_polling()
