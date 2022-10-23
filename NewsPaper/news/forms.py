from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post
from NewsPaper import settings


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'autor',
            'category_type',
            'post_category',
            'heading',
            'text',
        ]


'''class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(SignupForm, self).vave(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        html_content = render_to_string(
            'registration.html',
            {
                'user': user.name,
                'link': settings.SITE_URL,
            }
        )

        msg = EmailMultiAlternatives(
            subject='регистрация',
            body='',
            from_email='mviktor8208@yandex.ru',
            to=[f'{user.email}'],
        )
        print(user.email)
        print(user.name)
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
        return'''
