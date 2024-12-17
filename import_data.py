import json
import os
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")
django.setup()

from posts.models import Post
from django.contrib.auth.models import User

# Cargar datos del archivo original de backup
with open('original_backup.json', 'r', encoding='utf-8') as f:
    combined_data = json.load(f)

data_posts = combined_data['posts']
data_users = combined_data['users']
data_likes = combined_data['likes']

# Guardar datos de posts y users en la nueva base de datos
for post in data_posts:
    Post.objects.create(**post)

for user in data_users:
    User.objects.create(**user)

# Añadir el campo `date_like_it` y guardar los datos de likes
with connection.cursor() as cursor:
    for like in data_likes:
        like['date_like_it'] = "2024-01-01T00:00:00Z"  # Fecha predeterminada
        columns = ', '.join(like.keys())
        placeholders = ', '.join(['%s'] * len(like))
        sql = f"INSERT INTO posts_post_likes ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(like.values()))

print("Datos importados exitosamente desde original_backup.json")
