#-*- coding: utf-8 -*-
from app import app
from app import db
from flask import render_template,flash,request,session,redirect,url_for,abort
from flask.ext.bootstrap import Bootstrap
from app.forms import LoginForm,RegForm,ArticleForm
from article import Art
import hashlib 
import uuid
import logging
import datetime
from config import KEY

bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
	return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.route('/reg_bootstrap',methods = ['GET',"POST"])
def reg_bootstrap():
	# logging.error(request.method)
	form = RegForm(request.form)
	if request.method == "POST" :
		if form.validate():
			form.is_valid = True
			session['username'] = form.username.data
			session['email'] = form.email.data
			session['password'] = form.password.data
			db.connect()
			db.c.execute("INSERT INTO users VALUES (?,?,?,?)",
				(form.username.data,hashlib.md5(KEY+form.password.data).hexdigest(),form.email.data,'salt'))
			db.conn.commit()

			print "-"*100
			for user in db.c.execute('SELECT * FROM users').fetchall():
				print user
			return redirect(url_for('reg_success'))
		else:
			form.is_valid = False
			flash(u'请根据提示修改表单')
	return render_template('reg_bootstrap.html',form = form)


@app.route('/reg_success')
def reg_success():
	return render_template('reg_success.html',username = session.get('username'),email = session.get('email'),password = session.get('password'),)
	# pass

@app.route('/login_bootstrap',methods = ['POST','GET'])
def login_bootstrap():
	form = LoginForm(request.form)
	if request.method == "POST":
		if form.validate():
			#到数据库中查询,返回错误
			db.connect()
			logging.error('username = %s,psw = %s',form.username.data,form.password.data)
			db_password = db.c.execute("SELECT password FROM users WHERE username = ?",(form.username.data,)).fetchone()
			if db_password:
				if hashlib.md5(KEY + form.password.data).hexdigest() != db_password[0]:
					# print 'db_password =%s,input_psw = %s' %(db_password , hashlib.md5(KEY+form.password.data).hexdigest() ) 
					# logging.error('db_password = ',db_password)
					flash(u'密码错误')
				else:
					flash(u'登陆成功')
			else:
				logging.error(db_password)
				flash(u'用户名不存在')

	return render_template('login_bootstrap.html',form = form)

@app.route('/new',methods = ['GET',"POST"])
def new_art():
	db.connect()
	# logging.error()
	art = ArticleForm(request.form)
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

	db_query_arts = db.find_all('arts')
	arts = []
	for db_query_art in db_query_arts:
		arts.append(Art(db_query_art[0],db_query_art[1],db_query_art[2],db_query_art[3],db_query_art[4]))

	arts.reverse()
	return render_template('new_art.html',form = art,arts = arts)


@app.route('/articles/<art_id>')
def show_one_art(art_id):
	db.connect()
	result = db.c.execute('SELECT * FROM arts WHERE id = ?',(art_id,)).fetchone()
	if result:
		art = Art(result[0],result[1],result[2],result[3],result[4])
		return render_template('one_article.html',art = art) 
	else:
		# errorhandler('404')
		abort(404)
		# return redirect('/404')

@app.route('/art_list')
def show_art_list():
	db.connect()
	db_arts = db.c.execute('SELECT * FROM arts').fetchall()
	arts = []
	if db_arts:
		for db_art in db_arts:
			arts.append(Art(db_art[0],db_art[1],db_art[2],db_art[3],db_art[4]))
	return render_template('art_list.html',arts = arts,num =len(arts))

#2016年6月27日更新