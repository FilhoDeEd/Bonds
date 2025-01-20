from django.db import models
from user_profile.models import UserProfile
from django.utils import timezone
from forum.models import Forum

class Comment(models.Model):
    class TypeChoices(models.TextChoices):
        COMMENT = 'C', 'comment'
        REPORT = 'R', 'report'


    type = models.CharField(max_length=10, choices=TypeChoices.choices, default=TypeChoices.COMMENT)
    content = models.CharField(max_length=500)
    post_date = models.DateTimeField(auto_now_add=True) 
    # image = models.ForeignKey('ImageModel', on_delete=models.SET_NULL, null=True, blank=True)  
    denunciations = models.PositiveIntegerField(default=0)  

    ## confirmar esse on_delete CASCADE
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE) 

    def trust_rate(self):
        likes = self.likes.filter(is_like=True).count()
        dislikes = self.likes.filter(is_like=False).count()
        return likes - dislikes

    def __str__(self):
        return f'Comment: "{self.content}" by User {self.user_profile} in {self.forum}'

    class Meta:
        ordering = ['-post_date'] 

    def save(self, *args, **kwargs):
        if not self.id: 
            self.post_date = timezone.now()  
        
         ## pensar na ideia de fazer um controle de update por data
        ##self.update_date = timezone.now()
        
        super().save(*args, **kwargs)

    def get_like_count(self):
        return self.likes.count()

    def get_creator_name(self):
        """
        Retorna o nome completo do criador do comentário a partir do modelo Account, que está relacionado ao UserProfile.
        Se o usuário não estiver relacionado, retorna 'Sistema'.
        """
        if self.user_profile and self.user_profile.account: 
            return self.user_profile.account.full_name()  
        else:
            return 'Sistema'  


class Like(models.Model):
    comment = models.ForeignKey(Comment, related_name="likes", on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('comment', 'user_profile')

    def __str__(self):
        return f"Like by {self.user_profile} on Comment {self.comment.id}"
    
class Report(Comment):
    class TagChoices(models.TextChoices):
        SAUDE = 'SA', 'Saúde'
        LIXO = 'L', 'Lixo'
        INFRAESTRUTURA = 'I', 'Infraestrutura'
        SEGURANCA = 'SG', 'Segurança'
        EDUCACAO = 'E', 'Educação'
        TRANSPORTE = 'T', 'Transporte'
        ILUMINACAO = 'IL', 'Iluminação'
        OUTROS = 'O', 'Outros'

    tag = models.CharField(max_length=5, choices=TagChoices.choices, default=TagChoices.OUTROS)
    title = models.CharField(max_length=255)
    location = models.TextField(max_length=1023)
    solved = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now, editable=True)

class Pool(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=500)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, editable=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE) 

    class Meta:
        ordering = ['-post_date']

    def save(self, *args, **kwargs):
        if not self.id:  # Apenas na criação
            self.post_date = timezone.now()
        super().save(*args, **kwargs)


    def create_with_options(self, options):
        """
        Cria uma Pool e adiciona as opções associadas.
        :param options: Lista de strings representando as opções.
        """
        self.save()  # Salva a Pool
        for option_text in options:
            Option.objects.create(pool=self, option_text=option_text)

    def __str__(self):
        return self.title

class Option(models.Model):
    """
    Representa uma opção de resposta em uma enquete.
    """
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name="options")  
    option_text = models.CharField(max_length=255)  
    votes = models.PositiveIntegerField(default=0) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.option_text} ({self.votes} votos)"
    
class Vote(models.Model):

    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    option = models.ForeignKey(Option, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('user_profile', 'option')