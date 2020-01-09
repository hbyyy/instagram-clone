from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "아이디",
        }
    ))
    password = forms.CharField(max_length=20, label='', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '비밀번호',
        }
    ))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('username 또는 password가 올바르지 않습니다.')
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)
    # username.widget.attrs.update({'class': 'form-control'})
    # password.widget.attrs.update({'class': 'form-control'})
