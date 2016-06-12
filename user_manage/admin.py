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
        if not self.has_add_permission(request):
            raise PermissionDenied
        return TemplateResponse(request, 'admin/user_manage/user_add_list.html')


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)