from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField(
        required=True,
        # max_length=10,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username'})
    )
    password = forms.CharField(required=True)


    def clean(self):
        pass

