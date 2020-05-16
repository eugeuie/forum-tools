from django.contrib import admin

from .models import TashkentBoard, TashkentMember, TashkentMessage, TashkentTopic, Identifier, User, Message

admin.site.register(TashkentBoard)
admin.site.register(TashkentMember)
admin.site.register(TashkentMessage)
admin.site.register(TashkentTopic)
admin.site.register(Identifier)
admin.site.register(User)
admin.site.register(Message)
