#from django.urls import path
from rest_framework import routers
from .views import MessagesView


router = routers.DefaultRouter()
router.register('messages', MessagesView, 'messages')


urlpatterns = [

] + router.urls
