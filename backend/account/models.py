import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
import random


def directory_path(instance, filename):
    return f'images/profiles/{instance.id}/{filename}'


class Account(models.Model):
    class GendersChoices(models.TextChoices):
        FEMALE = 'F', 'Feminino'
        MALE = 'M', 'Masculino'
        OTHER = 'O', 'Outro'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birthday = models.DateField()
    gender = models.CharField(max_length=5, null=True, blank=True, choices=GendersChoices.choices)
    cellphone = models.CharField(max_length=255, null=True, blank=True)
    biography = models.CharField(max_length=4095, null=True, blank=True)
    agree_policy = models.BooleanField()
    profile_image = models.ImageField(upload_to=directory_path, null=True, blank=True)
    profile_image_low = models.ImageField(upload_to=directory_path, null=True, blank=True)

    email = models.EmailField(unique=True)
    email_notifications = models.BooleanField(default=True) # Pode vir direto no cadastro

    last_login = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True) # Usar isso onde?

    last_password_change = models.DateTimeField(null=True, blank=True)
    last_neighborhood_change = models.DateTimeField(null=True, blank=True)

    muted = models.BooleanField(default=False)
    mute_date = models.DateTimeField(null=True, blank=True)
    mute_days = models.IntegerField(null=True, blank=True)
    mute_count = models.IntegerField(default=0)

    suspension_reason = models.TextField(max_length=255, null=True, blank=True)

    join_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField()

    @property
    def login_active(self) -> bool:
        """
        Property method that returns whether the user's login is active.
        This is determined by the `is_active` status of the linked `User` model.
        """
        return self.user.is_active

    def mute(self, days: int) -> None:
        """
        Mutes the user for a specified number of days.
        
        Args:
            days (int): The number of days the user should be muted.
        """
        self.mute_count += 1
        self.muted = True
        self.mute_date = timezone.now()
        self.mute_days = days
        self.save()

    def unmute(self) -> None:
        """
        Unmutes the user by resetting the `muted`, `mute_date`, and `mute_days` fields.
        """
        self.muted = False
        self.mute_date = None
        self.mute_days = None
        self.save()

    def ban(self) -> None:
        """
        Bans the user by setting their `User` model's `is_active` field to `False`.
        This makes the user inactive and unable to log in.
        """
        self.user.is_active = False
        self.user.save()

    def unban(self) -> None:
        """
        Unbans the user by setting their `User` model's `is_active` field to `True`.
        This allows the user to log in again.
        """
        self.user.is_active = True
        self.user.save()

    def save(self, *args, **kwargs):
        """
        Override the `save` method to automatically set the `join_date` and update the `update_date`.
        The `join_date` is only set when the account is first created (i.e., no `id` exists).
        """
        if not self.id:
            self.join_date = timezone.now()
        self.update_date = timezone.now()
        return super().save(*args, **kwargs)
    
    def anonymize(self):
   
        with transaction.atomic():
            self.name = 'Anonymous'
            self.surname = 'User'
            self.birthday = '1970-1-1'
            self.gender = None
            self.cellphone = None
            self.biography = None

            # Hashing the email and adding a random number between 1 and 10000
            email_hash = hashlib.sha256(self.email.encode('utf-8')).hexdigest()
            random_number = random.randint(1, 100000)
            self.email = f'anonymous.{email_hash[:16]}_{random_number}@anonymous.invalid'

            self.last_login = None
            self.last_activity = None
            self.last_password_change = None
            self.last_neighborhood_change = None
            self.muted = False
            self.mute_date = None
            self.mute_days = None
            self.suspension_reason = None

            self.user.username = f'anonymous_{self.user.id}'
            self.user.set_unusable_password()
            self.user.is_active = False
            self.user.save()

            self.save()

    def full_name(self):
        """
        Returns the user's full name.
        """
        return self.name + ' ' + self.surname

    def __str__(self):
        """
        Returns the string representation of the `Account`, which is the username of the linked `User`.
        """
        return self.user.username
