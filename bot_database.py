# -*- coding: utf-8 -*-

import sqlite3

dbfile = 'data.db'

def init_db():
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS users (user_id integer primary key, request_step integer, request_string text)')
	conn.commit()
	conn.close()
	
def get_alldata():
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	c.execute('SELECT * FROM users')
	result = c.fetchall()
	conn.close()
	return result
	
def get_userdata(user_id):
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
	result = c.fetchone()
	conn.close()
	return result

def set_userdata(user_id, userdata):
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO users (user_id, request_step, request_string) VALUES(?, ?, ?)", (user_id, userdata.request_step, userdata.request_string))
	c.execute("UPDATE users SET request_step = ?, request_string = ? WHERE user_id = ?", (userdata.request_step, userdata.request_string, user_id))
	conn.commit()
	conn.close()
