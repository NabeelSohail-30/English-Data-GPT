from django.urls import path
from .views import view_chat, chat, export_messages_csv, view_chat_elastic, chatElastic, view_chat_fine, chatFine, view_chat_op

app_name = 'chat_openai'

urlpatterns = [
    path('view', view_chat, name='view'),
    path('chat', chat, name='chat'),
    path('viewElastic', view_chat_elastic, name='viewElastic'),
    path('chatElastic', chatElastic, name='chatElastic'),
    path('viewFine', view_chat_fine, name='viewFine'),
    path('chatFine', chatFine, name='chatFine'),
    path('viewChatOp', view_chat_op, name='viewChatOp'),
    path('export_messages_csv', export_messages_csv, name='export_messages_csv'),
]
