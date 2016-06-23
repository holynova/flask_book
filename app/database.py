#-*- coding: utf-8 -*-
import sqlite3
import os
import random
import datetime
import logging
import uuid
import hashlib
from config import KEY

class DB:
	def __init__(self,db_name='db.sql'):
		if not os.path.exists(db_name):
			print "new db ",db_name,' created'
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.db_name = db_name
		# self.creat_table()
		# self.random_insert()
	def connect(self):
		self.__init__(self.db_name)

	def creat_table(self,table_name='arts'):
		order = 'DROP TABLE IF EXISTS '+table_name
		self.c.execute(order)
		order = 'CREATE TABLE '+table_name+' (id text,title text,author text,content text,datetime text)'
		self.c.execute(order)

	def random_insert(self,table_name='arts',N=5):
		arts = []
		for i in range(N):
			art = (str(uuid.uuid1()),
				random.choice(u'个人日记 工作感悟 学习笔记 编程学习'.split())+str(i),
				random.choice(u'赵 钱 孙 李'.split())+random.choice(u'悟空 八戒 玄奘 悟净'.split()),
				u'我是正文',
				datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			arts.append(art)
		logging.error('%d articles added' %N)
		order = 'INSERT INTO '+ table_name+' VALUES (?,?,?,?,?)'
		self.c.executemany(order,arts)
		self.conn.commit()

	def insert_one(self,table_name,art_tuple):
		order = 'INSERT INTO '+ table_name+' VALUES (?,?,?,?,?)'
		self.c.execute(order,art_tuple)
		self.conn.commit()
		logging.error('a new line has been added to database.')

	def find_all(self,table_name = 'arts'):
		'''
		找到整个数据库中存储的数据,并返回
		返回值为一个obj, 但实际上是可以迭代的
		'''
		order = 'SELECT * FROM '+table_name
		return self.c.execute(order)
	def close(self):
		self.conn.close()


def db_init():
	db = DB(db_name = 'db.sql')
	db.creat_table(table_name = 'arts')
	db.random_insert('arts',9)

	# order = 'DROP TABLE IF EXISTS '+table_name
	db.c.execute("DROP TABLE IF EXISTS users")
	# order = 'CREATE TABLE '+table_name+' (id text,title text,author text,content text,datetime text)'
	db.c.execute("CREATE TABLE users (username text,password text,email text,salt text)")
	db.c.execute("INSERT INTO users VALUES (?,?,?,?)",('haha',hashlib.md5(KEY+'haha').hexdigest(),'admin@admin.com','salt'))
	db.c.execute("INSERT INTO users VALUES (?,?,?,?)",('user001',hashlib.md5(KEY+'haha').hexdigest(),'admin@admin.com','salt'))
	db.conn.commit() 
	db.close()
	return db
