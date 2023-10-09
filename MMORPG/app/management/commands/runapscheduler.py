import django.dispatch
import logging

logger = logging.getLogger(__name__)
weekly_mail = django.dispatch.Signal()


def send_digest():
    # Your job processing logic here...
    print("Job started")

    weekly_mail.send('send_digest')
    #   Signal.send('weekly_mail',)
    pass


