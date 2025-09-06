from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'chats', views.ChatViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'settings', views.UserSettingsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('', views.home_page, name='home'),  # New path for home page
]

