from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    contact = models.ForeignKey(User, related_name="contact", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"{self.user.username} ➜ {self.contact.username}"

    def __str__(self):
        return f"{self.user.username} ➜ {self.contact.username}"

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return " | ".join([u.username for u in self.participants.all()])

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    display_name = models.CharField(max_length=150, blank=True, null=True)  # добавь это поле

    def __str__(self):
        return self.user.username
