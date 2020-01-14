from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from members.models import User


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


class SignupForm(forms.Form):
    email = forms.EmailField(max_length=20, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email',
        }
    ))
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'username',
        }
    ))
    name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'name',
        }
    ))

    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
        }
    ))

    # def clean(self):
    #     username_check = User.objects.filter(username=self.cleaned_data['username']).exists()
    #     email_check = User.objects.filter(email=self.cleaned_data['email']).exists()
    #     if username_check is True:
    #         raise forms.ValidationError('이미 존재하는 username입니다')
    #     elif email_check is True:
    #         raise forms.ValidationError('이미 존재하는 email입니다')
    #     else:
    #         return self.cleaned_data

    def clean(self):
        print(f'{self.__class__.__name__}, clean')
        super().clean()

    def clean_email(self):
        print(f'{self.__class__.__name__}, clean_email')
        email_check = User.objects.filter(email=self.cleaned_data['email']).exists()
        if email_check is True:
            raise forms.ValidationError('이미 존재하는 email입니다')
        else:
            return self.cleaned_data['email']

    def clean_username(self):
        print(f'{self.__class__.__name__}, clean_username')
        username_check = User.objects.filter(username=self.cleaned_data['username']).exists()
        if username_check is True:
            raise forms.ValidationError('이미 존재하는 username입니다')
        else:
            return self.cleaned_data['username']

    def save(self):
        print(f'{self.__class__.__name__}, save')
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            # username=self.cleaned_username(),
            password=self.cleaned_data['password'],
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email']
            # email=self.clean_email()
        )
