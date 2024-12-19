import json
import os
import django
import sqlite3
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")
django.setup()

from posts.models import Post
from django.contrib.auth.models import User

def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

# Exportar datos de Post y User utilizando Django ORM
data_posts = list(Post.objects.values())
data_users = list(User.objects.values())

# Conectar directamente a la base de datos para exportar datos de likes
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Ejecutar una consulta para obtener todos los datos de likes
cursor.execute("SELECT * FROM posts_post_likes")
data_likes = cursor.fetchall()

# Obtener los nombres de las columnas
column_names = [description[0] for description in cursor.description]
data_likes_dicts = [dict(zip(column_names, row)) for row in data_likes]

conn.close()

# Combinar los datos en un solo archivo JSON
combined_data = {
    'posts': data_posts,
    'users': data_users,
    'likes': data_likes_dicts
}

# Escribir los datos serializados a un archivo
with open('original_backup.json', 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=4, default=convert_datetime)

print("Datos exportados exitosamente a original_backup.json")
