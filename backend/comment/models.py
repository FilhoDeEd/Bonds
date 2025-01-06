from django.db import models
from user_profile.models import UserProfile
from django.utils import timezone
from forum.models import Forum

class Comment(models.Model):
    """
    Modelo para representar um comentário em um fórum.
    """

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


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, related_name="likes", on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('comment', 'user_profile')

    def __str__(self):
        return f"Like by {self.user_profile} on Comment {self.comment.id}"