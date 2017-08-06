# -*- coding: utf-8 -*-

import sqlite3

DBFILE = 'data.db'

def init_db():
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS users (user_id integer primary key, username text, request_step integer, request_string text);')
	c.execute('CREATE TABLE IF NOT EXISTS bot_answers (user_id integer primary key, answer text, count integer, date integer);')
	#c.execute('ALTER TABLE users ADD username text;')
	conn.commit()
	conn.close()

def get_alldata():
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute('SELECT * FROM users;')
	result = c.fetchall()
	conn.close()
	return result

def get_userdata(user_id):
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE user_id=?;', (user_id,))
	result = c.fetchone()
	conn.close()
	return result

def set_userdata(user_id, userdata):
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO users (user_id, username, request_step, request_string) VALUES(?, ?, ?, ?);", (user_id, userdata.username, userdata.request_step, userdata.request_string))
	c.execute("UPDATE users SET request_step = ?, username = ?, request_string = ? WHERE user_id = ?;", (userdata.request_step, userdata.username, userdata.request_string, user_id))
	conn.commit()
	conn.close()
	
def get_answer(user_id):
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute('SELECT * FROM bot_answers WHERE user_id=?;', (user_id,))
	result = c.fetchone()
	conn.close()
	return result
	
def set_answer(user_id, answer):
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO bot_answers (user_id, answer, count, date) VALUES(?, ?, ?, ?);", (user_id, answer.answer.decode('utf-8'), answer.count, answer.date))
	c.execute("UPDATE bot_answers SET answer = ?, count = ?, date = ? WHERE user_id = ?;", (answer.answer.decode('utf-8'), answer.count, answer.date, user_id))
	conn.commit()
	conn.close()
	
def get_answers():
	conn = sqlite3.connect(DBFILE)
	c = conn.cursor()
	c.execute('SELECT * FROM bot_answers;')
	result = c.fetchall()
	conn.close()
	return result

