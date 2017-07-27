# -*- coding: utf-8 -*-

from telebot import types

from data import bot, Userdata, users, max_samepage_count, requestBasicText, logicalorrequest, allAgeRequest, getUsername, top100indexes
import texts
from texts import top100questions
from bot_log import log

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
