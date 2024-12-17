from django.contrib import admin
from .models import Post, Like

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
# Register your models here.
admin.site.register(Post, PostAdmin)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'date_like_it')
    search_fields = ('post__title', 'user__username')



