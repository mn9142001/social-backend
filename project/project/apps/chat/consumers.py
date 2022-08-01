import json
from channels.generic.websocket import AsyncWebsocketConsumer

#from .models import *
from user.models import User

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.userID = self.scope['user'].id
		self.room_group_name = f"user-{self.userID}"

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
		
	async def disconnect(self, close_code):
		# Leave room
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
	
	async def receive(self, text_data):
		data = json.loads(text_data)
		data['type'] = "chat_message"		
		# Send message to room group
		await self.channel_layer.group_send(self.room_group_name,data)

	# Receive message from room group
	async def chat_message(self, event):
		await self.send(text_data=json.dumps(event))
