from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from NewsPaper.settings import SITE_URL
from .models import PostCategory


def send_notifications(preview, pk, title, subcribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
           'text': preview,
           'link': f'{SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='mviktor8208@yandex.ru',
        to=subcribers,
    )

    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()  # отсылаем


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribes.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview, instance.pk, instance. heading, subscribers)


@receiver(post_save, sender=User)
def notify_about_new_user(sender, instance, **kwargs):
     name = instance.username
     male = instance.email
     print(male, name)

     html_content = render_to_string(
         'registration.html',
         {
             'user': name,
             'link': SITE_URL,
         }
     )

     msg = EmailMultiAlternatives(
         subject='регистрация',
         body='',
         from_email='mviktor8208@yandex.ru',
         to=[f'{male}'],
     )

     msg.attach_alternative(html_content, "text/html")  # добавляем html

     msg.send()  # отсылаем
