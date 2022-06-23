from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostLikes(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def user_logger(self, request):
        if request.user.is_authenticated:
            request.user.last_activity = datetime.datetime.now()
            request.user.save()
            return
        else:
            return

    def post(self, request):
        self.user_logger(request)
        post_item = get_object_or_404(Post, id=request.data['post_id'])

        try:
            like, created = Likes.objects.get_or_create(
                user_like=request.user,
                liked_post=post_item)

            if created:
                return JsonResponse(
                    {'status': 'The Post was liked'},
                    status=status.HTTP_201_CREATED)

            else:
                like.delete()
                return JsonResponse(
                    {'status': 'The Post was unliked'},
                    status=status.HTTP_202_ACCEPTED)

        except:
            return JsonResponse(
                {'status': 'Like does not work'},
                status=status.HTTP_400_BAD_REQUEST)


class PostsManage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def user_logger(self, request):
        if request.user.is_authenticated:
            request.user.last_activity = datetime.datetime.now()
            request.user.save()
            return
        else:
            return

    def post(self, request):
        self.user_logger(request)

        try:
            new_post, created = Post.objects.get_or_create(author=request.user, text=request.data['text'])

            if created:
                return JsonResponse(
                    {'status': 'Post created'},
                    status=status.HTTP_201_CREATED)

            else:
                return JsonResponse(
                    {'status': 'Post already exists'},
                    status=status.HTTP_302_FOUND)

        except:
            return JsonResponse(
                {'status': 'Post does not work'},
                status=status.HTTP_400_BAD_REQUEST)


class Analytics(generics.GenericAPIView):
    def get(self, request):
        try:
            dates = dict(request.query_params)

            like_count = Likes.objects.filter(like_datetime__range=[dates['date_from'][0], dates['date_to'][0]]).count()

            return JsonResponse(
                {'status': 'Received',
                 'like_by_period': f'{like_count}'},
                status=status.HTTP_200_OK)

        except:
            return JsonResponse(
                {'status': 'Analytics does not work'},
                status=status.HTTP_400_BAD_REQUEST)


class UserActivity(generics.GenericAPIView):
    def get(self, request):
        try:
            username = request.query_params['username']
            user = get_object_or_404(User, username=username)

            return JsonResponse(
                {'status': 'User found',
                 'last login': f'{user.last_login}',
                 'last activity': f'{user.last_activity}'},
                status=status.HTTP_200_OK
            )

        except:
            return JsonResponse(
                {'status': 'User Activity does not work'},
                status=status.HTTP_400_BAD_REQUEST)
