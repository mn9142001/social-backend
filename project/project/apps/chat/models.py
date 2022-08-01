from django.db import models

# Create your models here.


def MessageMediaStorage(instance, filename):
	return 'messages/room-{0}/{1}'.format(str(int(instance.message.sender.id) + int(instance.message.receiver.id)), filename)


def MessageRecordStorage(instance, filename):
	return 'messages/room-{0}/{1}'.format(str(int(instance.sender.id) + int(instance.receiver.id)), filename)


class Message(models.Model):
	states = ((1, 'sent'), (2, 'received'), (3, 'seen'))

	sender = models.ForeignKey('user.User', null=True, blank=True,
	                           on_delete=models.CASCADE, related_name='messages_sender')

	receiver = models.ForeignKey('user.User', null=True, blank=True,
	                             on_delete=models.CASCADE, related_name='messages_receiver')

	content = models.CharField(null=True, blank=True, max_length=255)
	record = models.FileField(
		null=True, blank=True, upload_to=MessageRecordStorage,)

	date = models.DateTimeField(auto_now_add=True)
	reply = models.ForeignKey('self', null=True, blank=True,
	                          on_delete=models.CASCADE, related_name='m_replies')
	state = models.IntegerField(default=1, choices=states)
	media = models.ManyToManyField('blog.SnippetFile', blank=True)

	def __str__(self):
		return str(self.content)

