from django import forms


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

    # username.widget.attrs.update({'class': 'form-control'})
    # password.widget.attrs.update({'class': 'form-control'})
