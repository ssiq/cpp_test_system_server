# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'errorlist'
    username = forms.CharField(max_length=254, label=u'用户名', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label=u'密码', required=True)


class ChangePasswordForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'errorlist'
    old_password = forms.CharField(widget=forms.PasswordInput, label=u'原密码', required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput, label=u'新密码', required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label=u'新密码确认', required=True)

    def clean(self):
        data = self.cleaned_data
        if data['new_password1'] != data['new_password2']:
            self.add_error('new_password1', u'第二次输入的新密码与此次不同')
        return super(ChangePasswordForm, self).clean()

