# -*- coding: utf-8 -*-
from flask import Flask,url_for,render_template,flash,request,session,redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import  BooleanField,StringField,SubmitField , TextField, PasswordField, validators
import logging

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
	password = PasswordField('New Password', [validators.Required(),validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField(u'我同意这个我从来没读过的用户协议', [validators.Required()])
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







if __name__=='__main__':
	app.run(debug=True)