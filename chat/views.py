from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message, Contact
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile
from django.http import HttpResponseForbidden
from .forms import ContactDisplayNameForm


@login_required
def profile_view(request, username=None):
    if username and username != request.user.username:
        profile_user = get_object_or_404(User, username=username)
        contact = Contact.objects.filter(user=request.user, contact=profile_user).first()
        if request.method == 'POST':
            if contact:
                form = ContactDisplayNameForm(request.POST, instance=contact)
            else:
                form = ContactDisplayNameForm(request.POST)
            if form.is_valid():
                contact_obj = form.save(commit=False)
                contact_obj.user = request.user
                contact_obj.contact = profile_user
                contact_obj.save()
                messages.success(request, "Имя в контактах сохранено.")
                return redirect('profile', username=username)
        else:
            if contact:
                form = ContactDisplayNameForm(instance=contact)
            else:
                form = None  
    else:
        profile_user = request.user
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile_user.profile)
            if form.is_valid():
                form.save()
                return redirect('profile_self')
        else:
            form = ProfileForm(instance=profile_user.profile)

    return render(request, 'chat/profile.html', {
        'profile_user': profile_user,
        'form': form,
    })

@login_required
def profile_view_by_id(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    contact = Contact.objects.filter(user=request.user, contact=profile_user).first()
    form = None

    if request.method == 'POST':
        if contact:
            form = ContactDisplayNameForm(request.POST, instance=contact)
        else:
            form = ContactDisplayNameForm(request.POST)
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.user = request.user
            contact_obj.contact = profile_user
            contact_obj.save()
            messages.success(request, "Имя в контактах сохранено.")
            return redirect('profile_by_id', user_id=user_id)
    else:
        if contact:
            form = ContactDisplayNameForm(instance=contact)
        else:
            form = ContactDisplayNameForm()

    return render(request, 'chat/profile.html', {
        'profile_user': profile_user,
        'form': form,
    })




@login_required
def index(request):
    chats = request.user.chats.all()
    contacts = Contact.objects.filter(user=request.user)
    contacts_map = {c.contact.id: c for c in contacts}

    return render(request, 'chat/index.html', {
        'chats': chats,
        'contacts_map': contacts_map,
        'user': request.user,
    })


@login_required
def create_chat(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            other_user = User.objects.get(username=username)
            existing_chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
            if existing_chat:
                return redirect('chat', chat_id=existing_chat.id)
            else:
                chat = Chat.objects.create()
                chat.participants.add(request.user, other_user)
                return redirect('chat', chat_id=chat.id)
        except User.DoesNotExist:
            return render(request, 'chat/create_chat.html', {'error': 'Пользователь не найден'})
    return render(request, 'chat/create_chat.html')


@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/contacts.html', {'contacts': contacts, 'users': users})

@login_required
def add_contact(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            contact_user = User.objects.get(username=username)
            if contact_user == request.user:
                messages.error(request, "Нельзя добавить себя в контакты.")
            else:
                obj, created = Contact.objects.get_or_create(user=request.user, contact=contact_user)
                if created:
                    messages.success(request, f"Пользователь {username} добавлен в контакты.")
                else:
                    messages.info(request, f"Пользователь {username} уже в контактах.")
            return redirect('contacts')
        except User.DoesNotExist:
            messages.error(request, f"Пользователь {username} не найден.")
            return redirect('add_contact')
    return render(request, 'chat/add_contact.html')
@login_required
def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participants.all():
        return redirect('index')

    contacts = Contact.objects.filter(user=request.user)
    contacts_map = {c.contact.id: c for c in contacts}

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(chat=chat, sender=request.user, text=text)
            return redirect('chat', chat_id=chat.id)

    messages = chat.messages.order_by('timestamp')

    return render(request, 'chat/chat.html', {
        'chat': chat,
        'messages': messages,
        'contacts_map': contacts_map,
    })


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_self')  
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})


@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user in chat.participants.all():
        if request.method == 'POST':
            chat.delete()
            return redirect('index')
        return render(request, 'chat/delete_chat_confirm.html', {'chat': chat})
    return HttpResponseForbidden("Вы не участник этого чата.")

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.user != message.sender:
        return HttpResponseForbidden("Вы можете редактировать только свои сообщения.")

    if request.method == 'POST':
        new_text = request.POST.get('text')
        message.text = new_text
        message.save()
        return redirect('chat', chat_id=message.chat.id)

    return render(request, 'chat/edit_message.html', {'message': message})


@login_required
def delete_message(request, msg_id):
    msg = get_object_or_404(Message, id=msg_id)
    if msg.sender != request.user:
        return HttpResponseForbidden("Вы не можете удалить это сообщение.")
    
    if request.method == 'POST':
        chat_id = msg.chat.id
        msg.delete()
        return redirect('chat', chat_id=chat_id)
    
    return render(request, 'chat/delete_message_confirm.html', {'message': msg})

@login_required
def chat_with_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
    return redirect('chat', chat_id=chat.id)

@login_required
def edit_contact_name(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactDisplayNameForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('profile_by_id', user_id=contact.contact.id)
    else:
        form = ContactDisplayNameForm(instance=contact)
    return render(request, 'chat/edit_contact_name.html', {'form': form})
