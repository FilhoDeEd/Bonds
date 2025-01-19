from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Sends a test email to verify email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient_email',
            type=str,
            help='The recipient email address for the test email'
        )

    def handle(self, *args, **kwargs):
        recipient_email = kwargs['recipient_email']
        subject = 'Test Email - Django'
        message = 'This is a test email sent from your Django application.'
        sender = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(subject, message, sender, [recipient_email], fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f'Test email successfully sent to {recipient_email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send test email: {e}'))
