from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import Chatroom, Message


# Create your views here.

def index(request):
    
    return render(request, 'index.html')


def room (request, room):
    username = request.GET.get('username')
    room_details = Chatroom.objects.get(room_name=room)
    return render(request, 'chatroom.html', {'room': room, 'username': username, 'room_details': room_details})

def checkview(request):
    room_name = request.POST['room_name']
    username = request.POST['username']

    if Chatroom.objects.filter(room_name = room_name).exists():
        return redirect(f'/room/{room_name}?username={username}')
    
    else:
        new_room = Chatroom.objects.create(room_name = room_name)
        new_room.save()
        return redirect(f"/room/{new_room}?username={username}")

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()

    return HttpResponse('Message sent successfully')
    

def getMessages(request, room):
    room_detail = Chatroom.objects.get(room_name=room)
    messages = Message.objects.filter(room = room_detail.id)

    return JsonResponse({'messages':list(messages.values())})

    