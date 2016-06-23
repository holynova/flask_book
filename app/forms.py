#-*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import BooleanField,StringField,SubmitField,TextAreaField,TextField,PasswordField,validators

class LoginForm(Form):
	username = TextField(u'用户名',[validators.DataRequired()],default ='user001' )
	password = PasswordField(u'密码',[validators.DataRequired()])
	save_user = BooleanField(u'记住密码',default = True)
	submit = SubmitField(u'登陆')

class RegForm(Form):
	username = TextField('user name',[validators.Length(min = 4,max=25,message =u'用户名长度限制:4到25个字符'),validators.DataRequired(u'不能空着')],default = 'user001')
	email = TextField('e-mail',[validators.Email(message = u"输入正确的e-mail")],default='user001@qq.com')
	password = PasswordField('New Password',[validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')],default='123456')
	confirm = PasswordField('Repeat Password',default='123456')
	accept_tos = BooleanField(u'我同意这个我从来没读过的用户协议', [validators.DataRequired()],default=True)
	submit = SubmitField('submit')

class ArticleForm(Form):
	title =  TextField(u'标题',[validators.DataRequired(),validators.Length(min = 1,max=25)],default = u"新文章标题")
	author =  TextField(u'作者',[validators.DataRequired(),validators.Length(min = 1,max=25)],default = u"孙悟空")
	content = TextAreaField(u'正文',[validators.DataRequired()],default = u"孙悟空到此一游。\n孙悟空故地重游\n")
	submit = SubmitField(u'发布')


