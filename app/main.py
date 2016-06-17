# -*- coding: utf-8 -*-
import logging
import sqlite3
import random,os
from flask import Flask,url_for,render_template,flash,request,session,redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import BooleanField,StringField,SubmitField,TextAreaField,TextField,PasswordField,validators
import uuid
import datetime


# from wrforms.validators import Required
# from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sangyimin'
bootstrap = Bootstrap(app)

class LoginForm(Form):
	# user_name = StringField("input your user name:",validators = [validators.DataRequired])
	user_name = StringField('Username', [validators.Length(min=4, max=25)])
	psw = PasswordField("input your password") 
	submit = SubmitField(u'提交')

class RegForm(Form):
	username = TextField('user name',[validators.Length(min = 4,max=25)])
	email = TextField('e-mail',[validators.Length(min=6, max=35)])
	password = PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField(u'我同意这个我从来没读过的用户协议', [validators.DataRequired()])
	submit = SubmitField('submit')
	def show(self):
		print "username = ",self.username.data
		print "email = ",self.email.data
		print "password = ",self.password.data
		print "confirm = ",self.confirm.data
		print "accept_tos = ",self.accept_tos.data
		

@app.route('/')
def index():
	# print dir(Form)
	# logging.error(dir(Form))
	return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.route('/user/<name>')
def user(name):
	print url_for('user',name = ' i am a <> fuckin & name')
	print url_for("list")
	return render_template('index.html',name = name)

@app.route('/list')
def list():
	return render_template('index.html',name = 'list')

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate():
		user_name = form.user_name.data
		psw = form.psw.data
		flash('Thanks for registering')
	else:
		user_name = "error_user_name"
		psw = "error_psw"
		flash('error')
	user_name = form.user_name.data
	psw = form.psw.data

	return render_template('login.html',form =form,user_name = user_name ,psw = psw)


@app.route('/reg',methods = ['GET','POST'])
def reg():
	form = RegForm(request.form)
	if request.method == "POST" and form.validate():
		# username = form.username
		# email = form.email
		# password = form.password
		flash('reg successd')
	else:
		flash('failed')
	form.show()
	return render_template("reg.html",form = form)



@app.route('/reg_bootstrap',methods = ['GET',"POST"])
def reg_bootstrap():
	
	form = RegForm(request.form)
	if request.method == "POST" :
		if form.validate():
			form.is_valid = True
			session['username'] = form.username.data
			session['email'] = form.email.data
			session['password'] = form.password.data
			
			# flash('reg successd')
			return redirect(url_for('reg_success'))

		else:
			form.is_valid = False
			flash(u'请根据提示修改表单')
	# elif request.method = "GET":

	return render_template('reg_bootstrap.html',form = form)


@app.route('/reg_success')
def reg_success():
	return render_template('reg_success.html',username = session.get('username'),email = session.get('email'),password = session.get('password'),)
	# pass

class Article(Form):
	title =  TextField(u'标题',[validators.DataRequired(),validators.Length(min = 1,max=25)],default = u"新文章标题")
	author =  TextField(u'作者',[validators.DataRequired(),validators.Length(min = 1,max=25)],default = u"孙悟空")
	content = TextAreaField(u'正文',[validators.DataRequired()],default = u"孙悟空到此一游\n孙悟空故地重游\n")
	submit = SubmitField(u'发布')

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
				random.choice(u'Zhao Qian Sun Li'.split())+'_'+random.choice('San Si Mazi'.split()),
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
		

class Art():
	def __init__(self,id,title,author,content,datetime):
		self.id = id
		self.title = title
		self.author = author
		self.content = content
		self.datetime = datetime


@app.route('/new',methods = ['GET',"POST"])
def new_art():
	db.connect()
	# logging.error()
	art = Article(request.form)
	# for a in art:
		# logging.error(a)
	
	if request.method == 'POST':
		if art.validate():
			#存入数据库
			db.insert_one(table_name = 'arts',
				art_tuple = (str(uuid.uuid1()),
				request.form['title'],
				request.form['author'],
				request.form['content'],
				datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
			# db.insert_one(table_name = 'arts',art_tuple = ('art.title',"art.author","art.content"))
			logging.error('new art added')

			#生成一个唯一的文章ID
			#跳转到单篇文章视图,显示预览

#step1 先用单页面实现数据库的存储和显示问题
#step2 改进成为有编辑页\文章单页\全部文章单独的页面的方式


	db_query_arts = db.find_all('arts')
	arts = []
	for db_query_art in db_query_arts:
		arts.append(Art(db_query_art[0],db_query_art[1],db_query_art[2],db_query_art[3],db_query_art[4]))
	#arts = 数据库中所有文章
	# db.close()
	arts.reverse()
	return render_template('new_art.html',form = art,arts = arts)


@app.route('/articles/<art_id>')
def show_one_art(art_id):
	db.connect()
	result = db.c.execute('SELECT * FROM arts WHERE id = "e5e91740-345d-11e6-afe8-f01faf28ea2d"')
	print '111111111111111111111111111111 result = ',result[0]
	for r in result:
		print '22222222222222222',r[0],r[1]
	if result:
		art = Art(result[0],result[1],result[2],result[3],result[4])
	return render_template('one_article.html',art = art) 


def db_init():
	db = DB(db_name = 'db.sql')
	db.creat_table(table_name = 'arts')
	db.random_insert('arts',2)
	db.close()
	return db



if __name__=='__main__':
	# init()
	db = db_init()
	app.run(debug=True)