from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Car, CarImage


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'style': 'color: white; background: #222; border: 1px solid #444; padding: 8px; width: 100%; border-radius: 5px;'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'style': 'color: white; background: #222; border: 1px solid #444; padding: 8px; width: 100%; border-radius: 5px;'
        })
    )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'phone', 'bio', 'avatar', 'telegram_chat_id']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'style': 'color: white; background: #222; padding: 5px; width: 100%; border-radius: 5px;'
            }),
            'phone': forms.TextInput(attrs={
                'style': 'color: white; background: #222; border: 1px solid #444; padding: 8px; width: 100%; border-radius: 5px;'
            }),
            'bio': forms.Textarea(attrs={
                'style': 'color: white; background: #222; border: 1px solid #444; padding: 8px; width: 100%; border-radius: 5px;',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'price', 'currency', 'description', 'image', 'power', 'transmission', 'acceleration', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
class MultipleImageForm(forms.Form):
    images = forms.FileField(required=False)