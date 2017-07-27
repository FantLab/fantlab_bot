# -*- coding: utf-8 -*-

import urllib2
import telebot #pip install pytelegrambotapi
from telebot import types
from BeautifulSoup import BeautifulSoup #pip install BeautifulSoup
import random
import re

from data import bot, Userdata, users, max_samepage_count, requestBasicText, logicalorrequest, allAgeRequest, getUsername, top100indexes
import texts
from texts import top100questions
from bot_log import log

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
