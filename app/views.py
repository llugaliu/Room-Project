from django.shortcuts import render, redirect
from .forms import SignUpForm, RoomForm, ProfileForm
from .models import Profile, Message, Room, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
    else:
        form = SignUpForm
    return render(request, 'app/signup.html', {'form': form})


@login_required(login_url='login')
def home(request):
    categories = Category.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        rooms = Room.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(description__icontains=q) |
            Q(category__title__icontains=q)
        )
        room_messages = Message.objects.filter(Q(room__category__title=q))

    else:
        rooms = Room.objects.all()
        room_messages = Message.objects.all()
    rooms_count = rooms.count()
    context = {
        'categories': categories,
        'rooms_count': rooms_count,
        'room_messages': room_messages,
        'rooms': rooms,
    }
    return render(request, 'app/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'app/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(title=category_name)
        Room.objects.create(
            host=request.user,
            category=category,
            name=request.POST.get('name'),
            description=request.POST.get('description')

        )
        messages.success(request, 'Room was created!')
        return redirect('/')
    return render(request, 'app/room_form.html', {'form': form, 'categories': categories})


@login_required(login_url='login')
def delete_room(request, pk):
    delete_room = Room.objects.get(pk=pk)
    delete_room.delete()
    messages.warning(request, 'Room was deleted!')
    return redirect('/')


@login_required(login_url='login')
def edit_room(request, pk):
    room = Room.objects.get(pk=pk)
    categories = Category.objects.all()
    form = RoomForm(instance=room)
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(title=category_name)
        Room.objects.create(
            host=request.user,
            name=request.POST.get('name'),
            category=category,
            description=request.POST.get('description')
        )
        messages.info(request, "Room was edited!")
        return redirect('/')
    else:
        form = RoomForm(instance=room)
    return render(request, 'app/edit_room.html', {'form': form, 'categories': categories, 'room': room})


@login_required(login_url='login')
def delete_message(request, pk):
    delete_message = Message.objects.get(pk=pk)
    delete_message.delete()
    messages.info(request, "Message was deleted!")
    return redirect('room', pk=delete_message.room.id)


@login_required(login_url='login')
def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    context = {
        'profile': profile
    }
    return render(request, 'app/profile.html', context)


@login_required(login_url='login')
def edit_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=profile.id)
    return render(request, 'app/edit_profile.html', {'form': form, 'profile': profile})
