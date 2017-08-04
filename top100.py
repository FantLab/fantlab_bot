# -*- coding: utf-8 -*-

from telebot import types

from data import bot, Userdata, users, getUsername, top100indexes
import texts
from texts import top100questions

def top100ArrayToString(index1, index2, array):
	if len(array) == 2:
		return str(array[1])
	return str(index1) + "\n" + str(index2)

def top100Func(message):
	message_chat_id = message.chat.id
	if not message_chat_id in users:
		users[message_chat_id] = Userdata(getUsername(message.chat), 0, "", None)
	keyboard = types.InlineKeyboardMarkup()
	localindex = top100indexes[message_chat_id] - 1
	k = 0
	for i in top100questions[localindex][2]:
		keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data="top100_goto\n" + top100ArrayToString(localindex, k, i)))
		k += 1
	keyboard.add(types.InlineKeyboardButton(text=texts.goback, callback_data="top100_goback " + str(top100questions[localindex][1])))
	bot.send_message(message_chat_id, top100questions[localindex][0], reply_markup=keyboard, parse_mode="Markdown")

def top100Result(message_chat_id, index1, index2):
	array = top100questions[index1][2][index2]
	result = array[3] + " *" + array[2] + "*\nhttps://fantlab.ru/work" + array[1]
	top100_button = types.InlineKeyboardButton(text=texts.showtop100AgainText, callback_data="/top100")
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(top100_button)
	bot.send_message(message_chat_id, result, reply_markup=keyboard, parse_mode="Markdown")
