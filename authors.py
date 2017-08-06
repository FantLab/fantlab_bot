# -*- coding: utf-8 -*-

import json
import urllib2
import urllib

from data import botSendMessage
import texts
from bot_log import log

AUTHORS_URL = 'https://api.fantlab.ru/search-autors.json?q='
authors = {}

def show_authors_invite(message):
	message_chat_id = message.chat.id
	authors[message_chat_id] = 1
	botSendMessage(message_chat_id, texts.AUTHORSREQUESTTEXT)


def show_authors_result(message):
	print(AUTHORS_URL + urllib.quote(message.text.encode('utf-8')))
	result = urllib2.urlopen(AUTHORS_URL + urllib.quote(message.text.encode('utf-8'))).read()
	log.debug(result)

def stop_authors_request(message_chat_id):
	authors[message_chat_id] = 0
