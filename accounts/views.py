from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
import random
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class RequestOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        
        try:
            user = User.objects.get(username=username)
            
            try:
                profile = user.userprofile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user, encrypted_info="Perfil generado automáticamente")
            
            otp = str(random.randint(100000, 999999))
            profile.otp_code = otp
            profile.otp_created_at = timezone.now()
            profile.save()

            print("\n" + "="*30)
            print(f"📧 SIMULADOR DE EMAIL 📧")
            print(f"Para: {user.email}")
            print(f"Tu código de recuperación es: {otp}")
            print("="*30 + "\n")

            return Response({'message': 'Código generado con éxito.'}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({'message': 'Si el usuario existe, se generó el código.'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(username=username)
            
            try:
                profile = user.userprofile
            except UserProfile.DoesNotExist:
                 return Response({'error': 'Perfil no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

            if profile.otp_code == otp:
                tiempo_limite = profile.otp_created_at + timedelta(minutes=5)
                
                if timezone.now() <= tiempo_limite:
                    user.set_password(new_password)
                    user.save()

                    profile.otp_code = None
                    profile.otp_created_at = None
                    profile.save()

                    return Response({'message': 'Contraseña actualizada con éxito.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'El código ha expirado. Solicitá uno nuevo.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Código inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)