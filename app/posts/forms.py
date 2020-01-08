from django import forms


class PostCreateForm(forms.Form):
    """
    이 Form에 들어갈 입력요소
        Image
        text
    """

    image = forms.ImageField()
    content = forms.CharField(max_length=200)

