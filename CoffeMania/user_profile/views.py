from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user

# Create your views here.
def show_user_profile(request):
    return render(request, 'user_profile/user_profile.html')

def editing_profile(request):

    user = request.user
    user.first_name = request.POST['first_name']
    user.username = request.POST['phone']
    user.email = request.POST['email']
    user.last_name = request.POST['adress']
    user.save()
    return JsonResponse({})