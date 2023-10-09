from .models import *
from datetime import date
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from .management.commands.runapscheduler import weekly_mail


@receiver(weekly_mail)
def weekly_mail(sender, **kwargs):
    current_site = Site.objects.get_current()
    site_link = f"http://{current_site.name}"
    Post.objects.filter(date_time__week=date.today().isocalendar()[1] - 1)
    if Post.count() > 0:
        hello_text = f'Здравствуй, {User}. Подборка статей за неделю на твоём любимом сайте !\n'
        header = 'Подборка статей за неделю'
        html_content = render_to_string('weekly_mail.html',
                                        {'header': header, 'hello_text': hello_text, 'site_link': site_link})
        msg = EmailMultiAlternatives(
            subject=f'{header}',
            body=hello_text,
            from_email=EMAIL_HOST_USER,
            to=[User.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
