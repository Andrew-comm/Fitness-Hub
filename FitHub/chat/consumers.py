# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the chat room named 'chat_room'
        self.room_name = 'chat_room'
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive a message from the WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']        
        # Get the sender's email
        sender_email = self.scope["user"].email
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp)

        
        
        # Broadcast the received message to everyone in the chat room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender_email': sender_email,
                'message': message,
                'timestamp': timestamp
            }
        )


    async def chat_message(self, event):
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'sender_email': event['sender_email'],
            'message': event['message']
        }))

