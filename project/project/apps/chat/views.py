from django.shortcuts import get_object_or_404
from user.models import User
from django.db.models import Q
from .serializers import MessageSerializer, MessageListSerializer
from rest_framework import viewsets
from .models import Message
from user.permissions import SnippetUpdateDeletePermission


class MessagesView(viewsets.ModelViewSet):
	serializer_class = MessageSerializer
	permission_classes = (SnippetUpdateDeletePermission, )
	queryset = Message.objects.all()

	def list(self, request):
		self.queryset = request.user.chatted_with.all()
		self.serializer_class = MessageListSerializer
		return super().list(request)

	def retrieve(self, request, pk):
		partner = get_object_or_404(User, pk=pk)
		self.queryset = Message.objects.filter((Q(receiver = request.user, sender = partner) | Q(sender=request.user, receiver = partner)))
		return super().list(request)
