# -*- coding: utf-8 -*-

import atexit
import sys
import traceback
import time
import threading
import requests

from data import bot, Userdata, users, answers, getUsername, top100indexes, botSendMessage, Answer
from authors import authors, show_authors_invite, show_authors_result, stop_authors_request
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
	res = db.get_answers()
	for obj in res:
		answers[obj[0]] = Answer(obj[1].encode('utf-8'), obj[2], obj[3])

def save_database():
	log.debug('Saving database, please wait.')
	for user in users:
		db.set_userdata(user, users[user]) #update database
	for answer_id in answers:
		db.set_answer(answer_id, answers[answer_id])
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
			botSendMessage(message_chat_id, texts.helpText)
		elif message_text == '/book':
			initData(message.chat)
			recomendationFunc(message)
		elif message_text == '/top100':
			initData(message.chat)
			top100Func(message)
		elif message_text == '/authors':
			show_authors_invite(message)
		elif authors[message_chat_id] == 1:
			show_authors_result(message)
		else:
			startFunc(message)
	except Exception as e:
		#TODO: forward messages when error happens: bot.forward_message(id, message_chat_id, message.message_id)
		log.debug('\nFailed: ' + message_text + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		botSendMessage(message_chat_id, texts.botErrorText)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			log.debug("Callback = " + call.message.text + " " + call.data)
			message_chat_id = call.message.chat.id
			if not message_chat_id in users:
				users[message_chat_id] = Userdata(getUsername(call.message.chat), 0, "", None)
			if call.data == '/book':
				initData(call.message.chat)
				recomendationFunc(call.message)
			elif call.data == 'wantanotherbook':
				users[message_chat_id].current_samepage_count += 1
				showResult(call.message)
			elif call.data == '/top100':
				initData(call.message.chat)
				top100Func(call.message)
			elif call.data.find("top100_goto") >= 0:
				data = call.data.split('\n')
				if len(data) == 2:
					top100indexes[message_chat_id] = int(data[1])
					top100Func(call.message)
				else:
					top100Result(message_chat_id, int(data[1]), int(data[2]))
			elif call.data.find("top100_goback") >= 0:
				data = call.data.split(' ')
				if data[1] == '0':
					top100indexes[message_chat_id] = int(data[1])
					startFunc(call.message)
				else:
					top100indexes[message_chat_id] = int(data[1])
					top100Func(call.message)
			else:
				data = call.data.split(' ')
				if users[message_chat_id].request_step != int(data[1]) + 1:
					users[message_chat_id].request_step -= 1
					recomendationFunc(call.message)
					return
				if data[0] != 'NONE': #собираем строку запроса
					users[message_chat_id].request_string += data[0]
				log.debug("Request string = " + str(message_chat_id) + " " + users[message_chat_id].request_string)
				if users[message_chat_id].request_step >= len(texts.requestStepsArray):
					botSendMessage(call.message.chat.id, texts.pleaseWaitText)
					showResult(call.message)
					return
				recomendationFunc(call.message)
	except Exception as e:
		log.debug('\nFailed: ' + call.data + "\r\n" + str(e) + "\r\n")
		log.error(traceback.format_exc())
		botSendMessage(call.message.chat.id, texts.botErrorText)

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

