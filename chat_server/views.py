from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from accounts.models import Profile
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User

from django.core import serializers



def get_login_users(request):

    users = list(User.objects.filter(profile__status=1).values_list('username', flat=True))
    print(users)
    print(json.dumps(users))



    return JsonResponse(json.dumps(users),safe=False)


def index(request):
    if not request.user.is_authenticated:

        print('not auth')
        return redirect('login')
    return render(request, 'chat_server/index.html', {})

def room(request, room_name):
    if not request.user.is_authenticated:
        print('not auth')
        return redirect('login')
    return render(request, 'chat_server/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })