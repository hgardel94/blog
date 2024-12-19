from django.db import models
from django.contrib.auth.models import User

# Create your models here

class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through="Like", related_name='post_likes', blank=True)
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_like_it = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'posts_post_likes'


