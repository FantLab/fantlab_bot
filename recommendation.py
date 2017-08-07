# -*- coding: utf-8 -*-

import random
import re
import urllib2
from telebot import types
from BeautifulSoup import BeautifulSoup #pip install BeautifulSoup

from data import Userdata, users, max_samepage_count, requestBasicText, logicalorrequest, allAgeRequest, getUsername, top100indexes, botSendMessage
import texts
from authors import stop_authors_request
from bot_log import log

def initData(chat):
	users[chat.id] = Userdata(getUsername(chat), 0, "", None)
	top100indexes[chat.id] = 1
	random.seed()

def startFunc(message):
	message_chat_id = message.chat.id
	stop_authors_request(message_chat_id)
	initData(message.chat)
	keyboard = types.InlineKeyboardMarkup()
	start_button = types.InlineKeyboardButton(text=texts.showRecomendsText, callback_data="/book")
	top100_button = types.InlineKeyboardButton(text=texts.showtop100Text, callback_data="/top100")
	authors_button = types.InlineKeyboardButton(text=texts.show_authors, callback_data="/authors")
	keyboard.add(start_button)
	keyboard.add(top100_button)
	keyboard.add(authors_button)
	botSendMessage(message_chat_id, texts.startText, reply_markup=keyboard)

def recomendationFunc(message):
	message_chat_id = message.chat.id
	if not message_chat_id in users:
		users[message_chat_id] = Userdata(getUsername(message.chat), 0, "", None)
	keyboard = types.InlineKeyboardMarkup()
	for i in texts.requestStepsArray[users[message_chat_id].request_step]:
		keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=i[1] + " " + str(i[2])))
	botSendMessage(message_chat_id, texts.requestNamesArray[users[message_chat_id].request_step], reply_markup=keyboard)
	users[message_chat_id].request_step += 1
	
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
	message_chat_id = message.chat.id
	if not message_chat_id in users:
		users[message_chat_id] = Userdata(getUsername(message.chat), 0, "", None)
	flag = False
	if users[message_chat_id].current_samepage_count == max_samepage_count:
		botSendMessage(message.chat.id, texts.pleaseWaitTheSameText)
		users[message_chat_id].current_samepage_count = 0
		users[message_chat_id].current_page += 1
		flag = True
	if users[message_chat_id].request_data is None or flag:
		if users[message_chat_id].request_string == "":
			users[message_chat_id].request_string = texts.fixRequestString
		users[message_chat_id].request_data = getData(requestBasicText + users[message_chat_id].request_string + logicalorrequest + "&page=" + str(users[message_chat_id].current_page))
	index = random.randint(3, len(users[message_chat_id].request_data) - 2)

	cols = users[message_chat_id].request_data[index].findAll('td')
	result = cols[0].getText(separator=u' ')
	result = re.sub(r"^\d+\. ", "", result)
	result = re.sub(' +', ' ', result)

	myre = re.compile(u'(\u00AB.*\u00BB)', re.UNICODE)
	result = myre.sub(r'*\1*', result)

	href = cols[0].findAll('a')[0]['href']
	href = "https://fantlab.ru" + re.findall("/work.*|$", href)[0]
	result = result + "\n" + href
	log.debug("Result = " + result)
	keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text=texts.iwantmoreText, callback_data="wantanotherbook")
	button2 = types.InlineKeyboardButton(text=texts.startagainText, callback_data="/book")
	keyboard.add(button1)
	keyboard.add(button2)
	botSendMessage(message.chat.id, result.encode('utf-8'), reply_markup=keyboard, parse_mode="Markdown")
