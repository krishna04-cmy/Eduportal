from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message, UserStatus

@login_required(login_url='/login/')
def chat_home(request):
    if request.user.is_staff:
        users = User.objects.exclude(id=request.user.id)
    else:
        users = User.objects.filter(is_staff=True)

    users_with_status = []
    for user in users:
        try:
            status = UserStatus.objects.get(user=user)
            is_online = status.is_online
        except UserStatus.DoesNotExist:
            is_online = False
        users_with_status.append({
            'user': user,
            'is_online': is_online,
        })

    return render(request, 'chat/chat_home.html', {
        'users_with_status': users_with_status,
    })

@login_required(login_url='/login/')
def chat_room(request, room_name):
    # room_name sirf dusre user ka naam hai
    users = sorted([request.user.username, room_name])
    actual_room_name = f"{users[0]}_{users[1]}"
    
    room, created = ChatRoom.objects.get_or_create(name=actual_room_name)
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50]

    try:
        other_user = User.objects.get(username=room_name)
        try:
            status = UserStatus.objects.get(user=other_user)
            is_online = status.is_online
        except UserStatus.DoesNotExist:
            is_online = False
    except User.DoesNotExist:
        other_user = None
        is_online = False

    return render(request, 'chat/chat_room.html', {
        'room_name': actual_room_name,  # ← sorted room name
        'messages': messages,
        'other_user': other_user,
        'is_online': is_online,
    })