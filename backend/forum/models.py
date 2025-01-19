from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from user_profile.models import Neighborhood, UserProfile
from django.db.models import Avg


class Forum(models.Model):
    class TypeChoices(models.TextChoices):
        DEFAULT = 'D', 'default'
        USER = 'U', 'user'
        EVENT = 'E', 'event'

    owner = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.PROTECT)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.PROTECT, editable=False)

    type = models.CharField(max_length=5, choices=TypeChoices.choices, default=TypeChoices.USER)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField(max_length=2047)

    # Campos de estatísticas (melhor fazer um cálculo complexo mas que não atulizar o tempo todo, somente de tempos em tempos)
        # Por hora, vamos só contar os inscritos
    subscribers_count = models.IntegerField(default=0)
    # posts_count = models.IntegerField(default=0) # Somente contar os comentários é falho (posso espamar em meu forum)
    # views_count = models.IntegerField(default=0) # Tem o mesmo problema do campo acima. É necessário um cálculo mais avançado

    # Controle de popularidade
    popularity = models.FloatField(default=0.0)  # Pode ser calculada no futuro

    # Controle de status (parece uma boa, mas n é necessário por agr) 
    #is_active = models.BooleanField(default=True) # Permitir ou não novos comentários
    #is_archived = models.BooleanField(default=False) # Remove o forum da visualização 

    # Campos de data
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField()

    # Sem banner por enquanto
    #banner = models.ImageField(upload_to='forum_banners/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = timezone.now()

        self.update_date = timezone.now()

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Forum.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def add_subscriber(self):
        """
        Adiciona um inscrito ao fórum.
        """
        self.subscribers_count += 1

    def remove_subscriber(self):
        """
        Remove um inscrito do fórum.
        """
        if self.subscribers_count > 0:
            self.subscribers_count -= 1

    def calculate_popularity(self):
        """
        Calcula popularidade com base em métricas do fórum.
        """
        self.popularity = self.subscribers_count * 10

    def get_creator_name(self):
        """
        TODO
        """
        if self.owner:
            return self.owner.account.full_name()
        else:
            return 'Sistema'

    def __str__(self):
        return self.title

class Event(Forum):

    date = models.DateField(editable=True)
    location = models.TextField(max_length=1023)
    cancelled = models.BooleanField(default=False)
    
    five_star_mean = models.FloatField(default=0.0)

    def calculate_five_star_mean(self):
       
        reviews = self.review_set.all()
        self.five_star_mean = reviews.aggregate(Avg('five_star'))['five_star__avg'] or 0.0
        self.save()

class Review(models.Model):

    FIVE_STAR_CHOICES = [
        (1, '1 - Terrível'),
        (2, '2 - Ruim'),
        (3, '3 - Regular'),
        (4, '4 - Bom'),
        (5, '5 - Excelente'),
    ]

    did_review = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    five_star = models.PositiveSmallIntegerField(choices=FIVE_STAR_CHOICES)
    review_date = models.DateTimeField(auto_now_add=True)
    
    def get_creator_name(self):
        """
        Retorna o nome completo do criador do comentário a partir do modelo Account, que está relacionado ao UserProfile.
        Se o usuário não estiver relacionado, retorna 'Sistema'.
        """
        if self.user_profile and self.user_profile.account: 
            return self.user_profile.account.full_name()  
        else:
            return 'Sistema'  

class Subscriber(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT, editable=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, editable=False)
    subscription_date = models.DateField(editable=False)
    is_sub = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.subscription_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_profile} | {self.forum} | {self.subscription_date}'
