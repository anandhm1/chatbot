# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from datetime import datetime
# # from .models import Message,ChatGroup
# # from django.contrib.auth.models import User


# class ChatConsumer(AsyncWebsocketConsumer):
                
#     async def connect(self):
#         self.group_name = self.scope['url_route']['kwargs']['group_name']
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         username = data['username']

#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': username,
#             }
#         )


#     async def chat_message(self, event):
#         from django.db import connection
#         current_time = datetime.utcnow()

#         # Format the current time to match the desired format
#         formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'username': event['username'],
#             'timestamp': formatted_time
#         }))
#         # with connection.cursor() as cursor:
#         #     cursor.execute("""SELECT * FROM chat_chatgroup WHERE name=%s""",(self.scope['url_route']['kwargs']['group_name']))
#         #     group_id = cursor.fetchone()[0]
#         #     cursor.execute("""SELECT * FROM auth_user WHERE username=%s""",(event['username']))
#         #     sender_id = cursor.fetchone()[0]
#         #     sql = """
#         #     INSERT INTO chat_message (content, timestamp, group_id, sender_id)
#         #     VALUES (%s, %s, %s, %s)
#         #     """
#         #     data = (event['message'], formatted_time, group_id,sender_id)
#         #     cursor.execute(sql, data)
#         # Fetch the required objects
#         # group = ChatGroup.objects.get(name=self.scope['url_route']['kwargs']['group_name'])
#         # sender = User.objects.get(username=event['username'])

#         # # Create a message instance
#         # message = Message(
#         #     group=group,
#         #     sender=sender,
#         #     content=event['message']
#         # )

#         # # Save to the database
#         # message.save() 
#     # @staticmethod
#     # async def save_message(sender_id, content):
#     #     sender = await User.objects.get(id=sender_id)
#     #     conversation = await ChatGroup.objects.get(id=self.conversation_id)
#     #     return await Message.objects.create(
#     #         conversation=conversation, sender=sender, content=content
#     #     )
    
import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

# from users.models import MyUser
# from .models import Message
# from .serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("here")
        self.room_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        # Send message to room group
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Receive message from room group
    def chat_message(self, event):
        from django.db import connection
        current_time = datetime.utcnow()
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        text_data_json = event.copy()
        text_data_json.pop("type")
        message, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM chat_chatgroup WHERE name=%s""",(self.room_name,))
            group_id = cursor.fetchone()[0]
            cursor.execute("""SELECT * FROM auth_user WHERE username=%s""",(event['username'],))
            sender_id = cursor.fetchone()[0]
            sql = """
            INSERT INTO chat_message (content, timestamp, group_id, sender_id)
            VALUES (%s, %s, %s, %s)
            """
            data = (event['message'], formatted_time, group_id,sender_id)
            cursor.execute(sql, data)

        # conversation = Conversation.objects.get(id=int(self.room_name))
        # sender = self.scope['user']

        # Attachment
        # if attachment:
        #     file_str, file_ext = attachment["data"], attachment["format"]

        #     file_data = ContentFile(
        #         base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
        #     )
        #     _message = Message.objects.create(
        #         sender=sender,
        #         attachment=file_data,
        #         text=message,
        #         conversation_id=conversation,
        #     )
        # else:
        #     _message = Message.objects.create(
        #         sender=sender,
        #         text=message,
        #         conversation_id=conversation,
        #     )
        # serializer = MessageSerializer(instance=_message)
        # # Send message to WebSocket
        # self.send(
        #     text_data=json.dumps(
        #         serializer.data
        #     )
        # )
  
        self.send(
            text_data=json.dumps(
                {
                     'message': event['message'],
            'username': event['username'],
            'timestamp': formatted_time
                }
            )
        )

