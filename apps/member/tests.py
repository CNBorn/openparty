# -*- coding: utf-8 -*-
from django.test import TestCase
from openparty.apps.member.models import Member
from openparty.apps.member.forms import SignupForm, LoginForm
import openparty.apps.member.test_helper as helper

class MemberTest(TestCase):
	def test_save_member_though_form(self):
			form = SignupForm({ 'email': 'some@domain.com', 'password1': '1', 'password2': '1' })
			member = form.save()
			self.assertTrue(isinstance(member, Member))
			self.assertTrue(member.user.id)

	def test_save_member_though_form_with_nickname(self):
		form = SignupForm({ 'email': 'some@domain.com', 'nickname': u'田乐', 'password1': '1', 'password2': '1' })
		member = form.save()
		self.assertTrue(member.user.id)

	def test_save_member_should_show_error_when_password_not_matching(self):
		form = SignupForm({ 'email': 'some@domain.com', 'password1': '1', 'password2': '2' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))

	def test_save_member_should_show_error_when_email_is_not_valid(self):
		form = SignupForm({ 'email': 'domain.com', 'password1': '1', 'password2': '1' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))

	def test_save_member_should_show_error_when_usernick_valid(self):
		form = SignupForm({ 'email': 'domain.com', 'password1': '1', 'nickname': '123456', 'password2': '1' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))
		form = SignupForm({ 'email': 'some@domain.com', 'password1': '1', 'nickname': 'Bei Jing', 'password2': '1' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))

	def test_login(self):
		helper.create_user()
		response = self.client.post('/login', {'email': 'tin@domain.com', 'password': '123'})
		self.assertRedirects(response, '/index')
	
	def test_login_should_failed_when_password_is_wrong(self):
		helper.create_user()
		response = self.client.post('/login', {'email': 'tin@domain.com', 'password': 'wrong-password'})
		self.assertFormError(response, 'form', '', u'您输入的邮件地址与密码不匹配或者帐号还不存在，请您重试或者注册帐号')
