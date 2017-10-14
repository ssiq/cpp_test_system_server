"""cpp_test_system_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url
from django.contrib import admin
from django.utils.translation import ugettext_lazy

import user_manage.views as user_manage_view
from django.conf.urls.static import static
import exams.views as exams_view
from utility.constant_value import *
import views
import settings

admin.site.site_header = ugettext_lazy('Cpp Test')
admin.site.index_title = ugettext_lazy('Cpp')
admin.site.site_title = ugettext_lazy('Cpp Test')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get_csrf/$', views.get_csrf_cookie),
    url(r'^check_version/$', views.check_version),
    # url(r'^download/(.+)/$', ),
    # TODO may change to include
    url(r'^%s/$' % register_students_url, user_manage_view.students_register_view),
    url(r'^%s/$' % register_one_student_url, user_manage_view.register_one_student_view),
    url(r'^%s/$' % login_url, user_manage_view.login_view),
    url(r'^%s/$' % logout_url, user_manage_view.logout_view),
    url(r'^%s/$' % create_exam_one_url, exams_view.create_exam_view),
    url(r'^%s/$' % get_exams_list_url, exams_view.get_exam_list_view),
    url(r'^%s/$' % get_active_exams_url, exams_view.get_active_exam_list_view),
    url(r'^%s/$' % get_one_exam_url, exams_view.get_one_exam_view),
    url(r'^%s/$' % create_one_question_url, exams_view.create_question_view),
    url(r'^%s/$' % download_exam_quesiton_view_url, exams_view.download_exam_question_view),
    url(r'^%s/$' % download_total_exam_url, exams_view.download_total_exam),
    url(r'^%s/$' % upload_exam_score_url, exams_view.upload_exam_score_view),
    url(r'^question/change/$', exams_view.change_question_view),
    url(r'^question/get_list/$', exams_view.get_question_list_view),
    url(r'^%s/$' % get_one_question_url, exams_view.get_question_view),
    url(r'^%s/$' % upload_exam_project_url, exams_view.upload_exam_log_project),
    url(r'^%s/$' % upload_exam_project_and_score_url, exams_view.upload_exam_log_project_score),

    url(r'^$', user_manage_view.web_login_view),
    url(r'^web/$', user_manage_view.web_home_view),
    url(r'^web/logout/$', user_manage_view.web_logout_view),
    url(r'^web/password_change/$', user_manage_view.web_change_password_view),
    url(r'^web/see_scores/$', exams_view.web_see_scores),
    url(r'^web/see_scores/(\d+)/$', exams_view.web_see_one_exam_score),
]

media_url = getattr(settings, 'MEDIA_URL', '/media/').lstrip('/')
urlpatterns.append(url(r'^%s(?P<path>.*)$' % media_url, 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }))