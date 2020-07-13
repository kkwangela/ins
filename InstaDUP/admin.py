from django.contrib import admin
from InstaDUP.models import Post, InstaUser, Like, UserConnection
# Register your models here.
admin.site.register(Post)
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(UserConnection)