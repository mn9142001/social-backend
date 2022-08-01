from django.db import models

def snippet_upload_path(instance, filename):
	return '{0}/{1}'.format(instance.__class__.__name__ ,filename)


class SnippetAbstract(models.Model):
	author 	= models.ForeignKey('user.User', null=True, blank=True, on_delete=models.CASCADE, related_name='%(class)s_author')
	content = models.CharField(max_length=5000, null=True, blank=True)
	date    = models.DateTimeField(auto_now_add=True)
	post 	= models.ForeignKey('Post', null=True, blank=True, on_delete=models.CASCADE, related_name='post_%(class)ss')
	reacts 	= models.ManyToManyField('React', blank=True, related_name='%(class)s_reacts')
	media 	= models.ManyToManyField('SnippetFile', blank=True, related_name='%(class)s_media')

	class Meta:
		abstract = True


class Post(SnippetAbstract):
	pass

class Comment(SnippetAbstract):
	reply	= models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='comment_replies')

class React(models.Model):
	_react = ((1, 'like'), (2, 'love'), (3,'haha'), (4,'wow'), (5,'sad'), (6,'angry'))
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True, related_name='user_reacts')
	react = models.IntegerField(choices=_react )

class SnippetFile(models.Model):
	media = models.FileField(upload_to=snippet_upload_path, blank=True, null=True)