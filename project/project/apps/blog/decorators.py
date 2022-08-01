from functools import wraps
from rest_framework.response import Response
from django.http import Http404
from .models import Post, Comment

def SnippetDecorator(function):
	@wraps(function)
	def wrap(request, *args, **kwargs):
		snippetID = int(request.data.get('snippetID'))
		try:
			snippet = Post.objects.get(pk=snippetID) if int(request.data.get('_snippet')) == 1 else Comment.objects.get(pk=snippetID)
		except snippet.DoesNotExist:
			raise Http404
		reacts = snippet.reacts.filter(user=request.user)
		if reacts.exists():
			reacts.delete()
			return Response({'react' : False})
		else:
			reacts.delete()

		kwargs['snippet'] = snippet
		return function(request, *args, **kwargs)
	return wrap