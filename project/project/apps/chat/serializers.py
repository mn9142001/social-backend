from rest_framework import serializers
from django.db.models import Q
from blog.models import SnippetFile
from user.serializers import SnippetAuthorSerializer
from .models import Message
from blog.serializers import SnippetFileSerializer

class BaseMessageSerializer(serializers.ModelSerializer):
	media = SnippetFileSerializer(required=False, many=True)
	sender = SnippetAuthorSerializer(default=serializers.CurrentUserDefault(), required = False)

	class Meta:
		model = Message
		abstract = True
		fields = ('id', 'content', 'date', 'record', 'reply', 'media', 'sender', 'receiver')

	@property
	def request(self):
		return self.context.get('request')

class MessageReply(BaseMessageSerializer):
	class Meta(BaseMessageSerializer.Meta):
		model = Message
		fields = BaseMessageSerializer.Meta.fields


class MessageSerializer(BaseMessageSerializer):

	class Meta(BaseMessageSerializer.Meta):
		fields = BaseMessageSerializer.Meta.fields

	def validate(self, validated_data):
		if not (validated_data.get('content', False), self.request.FILES.get('media', False)):
			return serializers.ValidationError("you cannot make blank messages.")
		return validated_data

	def create(self, data):
		_files = self.request.FILES.getlist('media')
		if _files:
			files = SnippetFile.objects.bulk_create([SnippetFile(media = file) for file in _files])
			data['media'] = files		
		obj = Message.objects.create(**data)
		return obj 

	def to_representation(self, instance):
		data = super().to_representation(instance)
		data['reply'] = MessageReply(instance).data
		return data

class MessageListSerializer(BaseMessageSerializer):
	last_m = serializers.SerializerMethodField(method_name='last_message')
	reply = MessageReply(required = False)

	class Meta(BaseMessageSerializer.Meta):
		fields = BaseMessageSerializer.Meta.fields + ('last_m',)


	def last_message(self, partner):
		user = self.request.user
		message =  MessageSerializer(Message.objects.filter((Q(receiver = user, sender = partner) | Q(sender=user, receiver = partner))).last()).data
		return message
