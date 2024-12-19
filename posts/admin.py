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





class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'liked_by')
    list_display = ('title', 'created', 'total_likes')

    def liked_by(self, obj):
        return ", ".join([str(user.username) for user in obj.likes.all()])

    liked_by.short_description = 'Liked By'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_like_it')


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)

