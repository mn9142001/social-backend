from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .models import Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
import os
from blog.models import SnippetFile

channel_layer = get_channel_layer()

@receiver(post_save, sender=Message)
def afterMessage(sender, instance, **kwargs):
    message = MessageSerializer(instance).data
    async_to_sync(channel_layer.group_send)(f"user-{message['sender']['id']}", {'messages' : message, 'type' : 'chat_message'})
    if message['receiver'] != message['sender']['id']:
        async_to_sync(channel_layer.group_send)(f"user-{message['receiver']}", {'messages' : message, 'type' : 'chat_message'})
    



@receiver(post_delete, sender=Message)
def afterMessageDelete(sender, instance, **kwargs):
    id = instance.id
    sender_id = instance.sender.id
    receiver_id = instance.receiver.id
    async_to_sync(channel_layer.group_send)(f"user-{sender_id}", {'deleted' : id, 'type' : 'chat_message'})
    if sender_id != receiver_id:
        async_to_sync(channel_layer.group_send)(f"user-{receiver_id}", {'deleted' : id, 'type' : 'chat_message'})

@receiver(post_delete, sender=SnippetFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.media:
        if os.path.isfile(instance.media.path):
            os.remove(instance.media.path)