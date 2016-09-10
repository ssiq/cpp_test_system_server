from django.http import JsonResponse
from django.contrib.auth.models import User
from utility.constant_value import ok_result, random_code
# Create your views here.
from utility.utility_funciton import generate_error_response, random_md5_hash


def add_one_student(username, password):
    user = User.objects.create_user(username)
    user.username = username
    user.password = password
    user.is_staff = False
    user.is_superuser = False
    user.is_active = True
    user.save()


def students_register_view(request):
    import pandas as pd
    f = request.FILES['student_list']
    try:
        data = pd.read_csv(f, names=['student_id', 'password'])
        for student_id, password in data.values:
            add_one_student(student_id, password)
        print 'register success'
        return JsonResponse(ok_result)
    except Exception, e:
        return JsonResponse(generate_error_response(e.message))


def register_one_student_view(request):
    try:
        student_id = request.POST['sid']
        if User.objects.filter(username=student_id):
            return JsonResponse(generate_error_response('user has registered'))
        else:
            password = request.POST['password']
            add_one_student(student_id, password)
            return JsonResponse(ok_result)
    except Exception, e:
        return JsonResponse(generate_error_response(e.message))


def login_view(request):
    from exams.models import ExitMd5
    try:
        username = request.POST['username']
        password = request.POST['password']
        used_key = request.POST['used_key']
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            new_login_result = {'new_login': False}
            new_login_result.update(ok_result)
            no_exit_login_result = {'new_login': True}
            no_exit_login_result.update(ok_result)
            if user.is_active:
                result = new_login_result
                if used_key != '':
                    l = ExitMd5.objects.filter(user=user)
                    if len(l) == 0 or str(l[0].md5) != str(used_key):
                        pass
                    else:
                        result = no_exit_login_result
                from django.contrib.auth import login
                login(request, user)
                request.session[random_code] = random_md5_hash()
                used_key = random_md5_hash()
                result['used_key'] = used_key
                for t in ExitMd5.objects.filter(user=user):
                    t.delete()
                o = ExitMd5.objects.create(user=user, md5=used_key)
                o.save()
                return JsonResponse(result)
            else:
                return generate_error_response('use is not active')
        else:
            return generate_error_response('username or password is wrong')
    except Exception, e:
            return JsonResponse(generate_error_response(e.message))


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return JsonResponse(ok_result)