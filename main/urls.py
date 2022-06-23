from django.urls import  path

from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('signup/', RegistrationAPIView.as_view(), name='signup'),

    path('post_like/', PostLikes.as_view(), name='post_like'),
    path('post_create/', PostsManage.as_view(), name='post_create'),
    path('analytics/', Analytics.as_view(), name='analytics'),
    path('user_activity/', UserActivity.as_view(), name='user_activity'),
]
