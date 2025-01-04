from django.db import models
from user_profile.models import UserProfile
from django.utils import timezone
from forum.models import Forum

class Comment(models.Model):
    """
    Modelo para representar um comentário em um fórum.
    """

    content = models.CharField(max_length=500)
    post_date = models.DateTimeField() 
    trust_rate = models.FloatField(default=0.0)
    # image = models.ForeignKey('ImageModel', on_delete=models.SET_NULL, null=True, blank=True)  
    denunciations = models.PositiveIntegerField(default=0)  

    ## confirmar esse on_delete CASCADE
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Relacionamento com o UserProfile
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)  # Relacionamento com o Forum

    def __str__(self):
        return f'Comment: "{self.content}" by User {self.user_profile} in {self.forum}'

    class Meta:
        ordering = ['-post_date']  # Ordenação dos comentários pela data de postagem

    def save(self, *args, **kwargs):
        if not self.id: 
            self.post_date = timezone.now()  
        
         ## pensar na ideia de fazer um controle de update por data
        ##self.update_date = timezone.now()
        
        super().save(*args, **kwargs)

    def get_creator_name(self):
        """
        Retorna o nome completo do criador do comentário a partir do modelo Account, que está relacionado ao UserProfile.
        Se o usuário não estiver relacionado, retorna 'Sistema'.
        """
        if self.user_profile and self.user_profile.account:  # Verificando se existe o user_profile e o account
            return self.user_profile.account.full_name()  # Acessa o nome completo através do campo account
        else:
            return 'Sistema'  # Retorna 'Sistema' caso não exista o user_profile ou o account
