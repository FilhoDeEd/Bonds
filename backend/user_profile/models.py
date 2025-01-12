from account.models import Account
from django.db import models
from django.utils import timezone


class UfChoices(models.TextChoices):
    AC = 'AC', 'Acre'
    AL = 'AL', 'Alagoas'
    AP = 'AP', 'Amapá'
    AM = 'AM', 'Amazonas'
    BA = 'BA', 'Bahia'
    CE = 'CE', 'Ceará'
    DF = 'DF', 'Distrito Federal'
    ES = 'ES', 'Espírito Santo'
    GO = 'GO', 'Goiás'
    MA = 'MA', 'Maranhão'
    MT = 'MT', 'Mato Grosso'
    MS = 'MS', 'Mato Grosso do Sul'
    MG = 'MG', 'Minas Gerais'
    PA = 'PA', 'Pará'
    PB = 'PB', 'Paraíba'
    PR = 'PR', 'Paraná'
    PE = 'PE', 'Pernambuco'
    PI = 'PI', 'Piauí'
    RJ = 'RJ', 'Rio de Janeiro'
    RN = 'RN', 'Rio Grande do Norte'
    RS = 'RS', 'Rio Grande do Sul'
    RO = 'RO', 'Rondônia'
    RR = 'RR', 'Roraima'
    SC = 'SC', 'Santa Catarina'
    SP = 'SP', 'São Paulo'
    SE = 'SE', 'Sergipe'
    TO = 'TO', 'Tocantins'


class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=UfChoices.choices)
    country = models.CharField(max_length=255, default='Brazil')

    create_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'state', 'locality', 'country'],
                name='unique_neighborhood'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_date = timezone.now()
        self.update_date = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}, {self.locality}, {self.state}'


class UserProfile(models.Model):
    class StatusChoices(models.TextChoices):
        NEWCOMER = 'newcomer', 'Recém Chegado'
        CURIOUS_NEIGHBOR = 'curious', 'Vizinho Curioso'
        ATTENTIVE_NEIGHBOR = 'attentive', 'Vizinho Atento'
        COLLABORATIVE_NEIGHBOR = 'collaborative', 'Vizinho Colaborador'
        TRUSTWORTHY_NEIGHBOR = 'trustworthy', 'Vizinho Confiável'
        NOTABLE_NEIGHBOR = 'notable', 'Vizinho Notável'
        INSPIRING_NEIGHBOR = 'inspiring', 'Vizinho Inspirador'
        NEIGHBORHOOD_GUARDIAN = 'guardian', 'Guardião do Bairro'
        COMMUNITY_SAGE = 'sage', 'Sábio da Comunidade'

    trust_rate = models.FloatField(default=100.0)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=31, choices=StatusChoices.choices, default=StatusChoices.NEWCOMER)

    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.PROTECT)

    create_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_date = timezone.now()

        self.update_status()

        self.update_date = timezone.now()
        super().save(*args, **kwargs)

    def update_status(self):
        """
        Atualiza o status do usuário com base no tempo desde a criação do perfil.
        """
        days_active = (timezone.now() - self.create_date).days
        if days_active < 30:
            self.status = self.StatusChoices.NEWCOMER
        elif days_active < 90:
            self.status = self.StatusChoices.CURIOUS_NEIGHBOR
        elif days_active < 180:
            self.status = self.StatusChoices.ATTENTIVE_NEIGHBOR
        elif days_active < 365:
            self.status = self.StatusChoices.COLLABORATIVE_NEIGHBOR
        elif days_active < 730:
            self.status = self.StatusChoices.TRUSTWORTHY_NEIGHBOR
        elif days_active < 1095:
            self.status = self.StatusChoices.NOTABLE_NEIGHBOR
        elif days_active < 1460:
            self.status = self.StatusChoices.INSPIRING_NEIGHBOR
        elif days_active < 1825:
            self.status = self.StatusChoices.NEIGHBORHOOD_GUARDIAN
        else:
            self.status = self.StatusChoices.COMMUNITY_SAGE

    def __str__(self):
        if self.account:
            return f'{self.account.user.username} | {self.id}'
        return f'Anonymous | {self.id}'
