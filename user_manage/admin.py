# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.template.response import TemplateResponse


class MyUserAdmin(UserAdmin):
    change_list_template = 'admin/user_manage/user_change_list.html'

    def get_urls(self):
        return [
                   url(
                       r'^add_list/$',
                       self.admin_site.admin_view(self.add_user_list),
                       name='auth_add_user_list',
                   ),
               ] + super(UserAdmin, self).get_urls()

    def add_user_list(self, request):
        import pandas as pd
        from django.contrib.auth.models import User
        if not self.has_add_permission(request):
            raise PermissionDenied
        user_file = request.FILES.get('user_list', None)
        firstin = request.POST.get('firstin', True)
        if user_file is None:
            print 'nofile'
        else:
            firstin = False
            error = []
            try:
                user_dataframe = pd.read_csv(user_file)
                for k in ['username', 'password']:
                    if k not in user_dataframe:
                        raise Exception(u"不存在列名是{}的列".format(k))

                if len(user_dataframe['username']) != len(set(user_dataframe['username'])):
                    print 'exit same username'
                    error = u'csv文件中存在用户名相同的用户'
                for username, password in zip(user_dataframe['username'], user_dataframe['password']):
                    user = User.objects.filter(username=username)
                    if len(user) != 0:
                        print 'user {} has exists'.format(username)
                        error.append(u"用户{}已经存在".format(username))
                if len(error) == 0:
                    for username, password in zip(user_dataframe['username'], user_dataframe['password']):
                        user = User.objects.create_user(username=username, password=password)
                        user.is_staff = False
                        user.is_superuser = False
                        user.is_active = True
                        user.save()

            except Exception, e:
                print u"{}".format(e)
                error.append(u'csv文件格式错误:{}'.format(e.message))

            if len(error) != 0:
                error.append(u"请仔细检查csv文件中的内容，然后重新提交")
        show_success = ((not firstin) and (len(error) == 0))
        return TemplateResponse(request, 'admin/user_manage/user_add_list.html', locals())


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)