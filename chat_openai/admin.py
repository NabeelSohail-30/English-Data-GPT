from django.contrib import admin
from .models import OpenAiMessage
from .model_message import Messages
from .modelElastic import ElasticChat
from .modelElasticMessages import ElasticMessages
from .modelFine import FineChat
from .modelFineMessages import FineMessages

# Register your models here.
admin.site.register(OpenAiMessage)
admin.site.register(Messages)
admin.site.register(ElasticChat)
admin.site.register(ElasticMessages)
admin.site.register(FineChat)
admin.site.register(FineMessages)
