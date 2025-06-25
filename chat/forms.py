from django import forms
from .models import Contact, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class ContactDisplayNameForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['display_name']
        widgets = {
            'display_name': forms.TextInput(attrs={'placeholder': 'Имя в контактах'}),
        }
        labels = {
            'display_name': 'Имя в контактах',
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'avatar']
        labels = {
            'display_name': 'Имя',
            'avatar': 'Аватар',
        }
