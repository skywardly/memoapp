from django import forms
from django.core.exceptions import ValidationError
from .models import MemoModel

class LoginForm(forms.Form):
    username = forms.EmailField(
        required=True,
        # max_length=10,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username'})
    )
    password = forms.CharField(required=True)


    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username == 'hogehoge' and password == 'hogehoge':
            raise ValidationError('ユーザ名がhogehogeかつパスワードがhogehogeはログインできません。')
        return 


class MemoForm(forms.ModelForm): # ModelFormを継承
    class Meta():
        model = MemoModel # どのmodelを利用するかmodel = モデル名で定義
        fields = ('memo',) # 表示するフィールド、'__all__'とすると全て


'''
class MemoForm(forms.Form):
    memo = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )
'''


'''
    a = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a = 2
        print('__init__')

    def clean_memo(self):
        self.a = 1
        a = 1
        print('clean_memo')
        print(self.a)
        
        data = self.cleaned_data['memo']
        if data.startswith('1'):
            self.add_error('memo', '１で始まってはだめです')
            #raise ValidationError('１で始まってはだめです')
        if data.endswith('2'):
            self.add_error('memo', '２で終わってはだめです')
            #raise ValidationError('２で終わってはだめです')
        return data
'''