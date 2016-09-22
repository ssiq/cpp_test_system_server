# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'errorlist'
    username = forms.CharField(max_length=254, label=u'用户名', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label=u'密码', required=True)

