from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):
    """
    Aggregates user account information and provides methods to manage user states.

    Fields:
    --------
    - **user (OneToOneField)**: A one-to-one relationship with the `User` model. Links the account to the user.
      Deleting the user cascades and deletes the associated account.
    - **active_user_profile (OneToOneField)**: A one-to-one relationship with the `UserProfile` model. Links the account to the
      currenty user profile.
    - **name (CharField)**: The user's first name.
    - **surname (CharField)**: The user's last name.
    - **birthday (DateField)**: The user's date of birth.
    - **cellphone (CharField)**: The user's cellphone number, optional and stored as a string for format flexibility.
    - **agree_policy (BooleanField)**: Indicates whether the user has agreed to the platform's policies. Must be `True` for account activation.
    - **email (EmailField)**: The user's email address, unique to each account.
    - **email_notifications (BooleanField)**: Indicates whether the user allows email notifications. Defaults to `True`.
    - **last_login (DateTimeField)**: The date and time of the user's last login. Can be `null` if the user never logged in.
    - **last_activity (DateTimeField)**: The date and time of the user's last recorded activity. Can be `null` if no activity is logged.
    - **last_password_change (DateTimeField)**: The last date and time the user changed their password. Optional.
    - **last_neighborhood_change (DateTimeField)**: Tracks when the user last changed their neighborhood. Optional.
    - **muted (BooleanField)**: Indicates if the user is muted. Defaults to `False`.
    - **mute_date (DateTimeField)**: The date and time when the user was muted. Optional.
    - **mute_days (IntegerField)**: Number of days the user will remain muted. Optional.
    - **mute_count (IntegerField)**: The total number of times the user has been muted. Defaults to `0`.
    - **suspension_reason (TextField)**: Explains the reason for account suspension. Optional.
    - **join_date (DateTimeField)**: The date and time when the account was created. Automatically set during creation.
    - **update_date (DateTimeField)**: The last date and time the account was updated. Automatically updated on each save.

    Methods:
    --------
    - **login_active (property)**: Returns `True` if the associated `User` is active, otherwise `False`.
    - **set_active_user_profile(user_profile: UserProfile)**: Change active user profile.
    - **mute(days: int)**: Mutes the user for a given number of days and updates mute-related fields.
    - **unmute()**: Unmutes the user by resetting mute-related fields (`muted`, `mute_date`, `mute_days`).
    - **ban()**: Deactivates the user by setting their `User`'s `is_active` field to `False`.
    - **unban()**: Reactivates the user by setting their `User`'s `is_active` field to `True`.
    - **save(*args, **kwargs)**: Overrides the `save` method to set `join_date` during creation and update `update_date` on every save.
    - **__str__()**: Returns the username of the associated `User`.

    Notes:
    ------
    This model serves as an extended profile for users, encapsulating additional account-specific data
    beyond what is provided by Django's default `User` model.
    """
    class GendersChoices(models.TextChoices):
        FEMALE = 'F', 'Feminino'
        MALE = 'M', 'Masculino'
        OTHER = 'O', 'Outro'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #active_user_profile = models.OneToOneField('user_profile.models.UserProfile', on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birthday = models.DateField()
    gender = models.CharField(max_length=5, null=True, blank=True, choices=GendersChoices.choices)
    cellphone = models.CharField(max_length=255, null=True, blank=True)
    biography = models.CharField(max_length=4095, null=True, blank=True)
    agree_policy = models.BooleanField()

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

    # def set_active_user_profile(self, user_profile: UserProfile):
    #     """
    #     Set active UserProfile.

    #     Args:
    #         user_profile (UserProfile): The new active UserProfile.
    #     """
    #     if self.active_user_profile:
    #         self.active_user_profile.active = False
    #         self.active_user_profile.save()
        
    #     self.active_user_profile = user_profile
    #     user_profile.active = True
    #     user_profile.save()
    #     self.save()

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

    def unmute(self) -> None:
        """
        Unmutes the user by resetting the `muted`, `mute_date`, and `mute_days` fields.
        """
        self.muted = False
        self.mute_date = None
        self.mute_days = None

    def ban(self) -> None:
        """
        Bans the user by setting their `User` model's `is_active` field to `False`.
        This makes the user inactive and unable to log in.
        """
        self.user.is_active = False

    def unban(self) -> None:
        """
        Unbans the user by setting their `User` model's `is_active` field to `True`.
        This allows the user to log in again.
        """
        self.user.is_active = True

    def save(self, *args, **kwargs):
        """
        Override the `save` method to automatically set the `join_date` and update the `update_date`.
        The `join_date` is only set when the account is first created (i.e., no `id` exists).
        """
        if not self.id:
            self.join_date = timezone.now()
        self.update_date = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the string representation of the `Account`, which is the username of the linked `User`.
        """
        return self.user.username
