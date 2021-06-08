from django import forms
from .models import TBUsers
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    user_id = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        },
        max_length=32, label="사용자 ID")
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label="비밀번호")

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')


        if user_id and password:
            try:
                user_id = TBUsers.objects.get(user_id=user_id)
            except TBUsers.DoesNotExist:
                self.add_error('user_id', '아이디가 없습니다')
                return

            #if not check_password(password, user_id.password):   # 암호화 나중에 처리
            if not password == user_id.password:
                self.add_error('password', '비밀번호를 틀렸습니다')
            else:
                self.user_id = user_id.user_id
