import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser

from .permissions import IsAdministrator
from .serializers import CreateUserSerializer, CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    permission_classes = [IsAdministrator]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        email = request.user.email
        user = CustomUser.objects.get(email=email)
        if request.method == 'GET':
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CustomUserCreateViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        email = self.request.POST.get('email')
        confirmation_code = random.uniform(0, 40)
        send_mail(
            subject='Confirmation code',
            message=str(confirmation_code),
            from_email='admin@gmail.com',
            recipient_list=[email]
        )
        serializer.save(confirmation_code=confirmation_code)


class CreateToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.POST.get('email')
        user = get_object_or_404(CustomUser, email=email)
        get_confirmation_code = request.POST.get('confirmation_code')

        if user.confirmation_code == get_confirmation_code:
            refresh = RefreshToken.for_user(request.user)
            return Response(
                {
                    'access': str(refresh.access_token),
                }
            )
        return Response(
            {'message': 'Bad confirmation_code'},
            status=status.HTTP_400_BAD_REQUEST
        )
