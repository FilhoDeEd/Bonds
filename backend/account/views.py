import os

from io import BytesIO
from account.models import Account
from account.serializers import AccountSerializer, UserSerializer, UpdateAccountBaseSerializer
from PIL import Image
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta
from django.utils.timezone import now

from user_profile.serializers import UserProfileSerializer, NeighborhoodSerializer
from user_profile.models import Neighborhood, UserProfile



MAX_FILE_SIZE = 5 * 1024 * 1024


def add_errors(errors: Dict, serializer_errors: Dict):
    for field, error in serializer_errors.items():
        if field in errors:
            errors[field].extend(error)
        else:
            errors[field] = error


def send_custom_email(subject: str, email: str, template_name: str, context: Dict[str, Any]):
    try:
        html_message = render_to_string(template_name=template_name, context=context)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(
            subject=subject,
            message='',
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False
        )
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")


class RegisterView(APIView):
    """
    Handles user create account.
    """
    def post(self, request):
        data = request.data

        user_data = {
            'username': data.pop('username', ''),
            'password': data.pop('password', ''),
        }

        neighborhood_id = data.pop('neighborhood', None)

        errors = {}

        if not neighborhood_id:
            errors['neighborhood'] = 'This field is required.'

        user_serializer = UserSerializer(data=user_data)
        account_serializer = AccountSerializer(data=data)

        if not user_serializer.is_valid():
            add_errors(errors=errors, serializer_errors=user_serializer.errors)

        if not account_serializer.is_valid():
            add_errors(errors=errors, serializer_errors=account_serializer.errors)
        
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        except Neighborhood.DoesNotExist:
            return Response({'neighborhood': 'Invalid neighborhood ID.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user = user_serializer.save()
                account = account_serializer.save(user=user)
                UserProfile.objects.create(account=account, neighborhood=neighborhood)
                Token.objects.create(user=user)
        except IntegrityError as e:
            return Response({'detail': f'Database error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        send_custom_email('Bem-vindo ao Bonds!', account.email, 'welcome_email.html', {'account': account})

        return Response({'detail': 'Account successfully created.'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Handles user login requests.
    """
    def post(self, request):
        username = request.data.get('emailOrUsername', '').strip()
        password = request.data.get('password', '').strip()

        if not username or not password:
            return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials.')

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'access': token.key}, status=status.HTTP_200_OK)


class DetailAccountView(APIView):
    """
    Handles requests for user personal details.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            account = user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
            user_profile.update_status()
            user_profile.save()
            neighborhood = user_profile.neighborhood

            user_serializer = UserSerializer(user)
            account_serializer = AccountSerializer(account, context={'request': request})
            user_profile_serializer = UserProfileSerializer(user_profile)
            neighborhood_serializer = NeighborhoodSerializer(neighborhood)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {}
        data |= user_serializer.data
        data |= account_serializer.data
        data |= user_profile_serializer.data
        data |= neighborhood_serializer.data
        
        return Response(data, status=status.HTTP_200_OK)


class UpdateAccountBaseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        account = request.user.account

        serializer = UpdateAccountBaseSerializer(account, data=data)

        errors = {}

        if not serializer.is_valid():
            add_errors(errors=errors, serializer_errors=serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                serializer.save()
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Basic account details updated successfully.'}, status=status.HTTP_200_OK)


class UpdateAccountEmailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account = request.user.account
        new_email = request.data.get('email', '').strip()

        if not new_email:
            return Response({'email': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_email(new_email)
        except ValidationError:
            return Response({'email': 'Enter a valid email address.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                account.email = new_email
                account.save()
        except IntegrityError:
            return Response({'email': 'This email address is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'detail': 'Account email updated successfully.'}, status=status.HTTP_200_OK)


class UpdateAccountPasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account = request.user.account
        new_password = request.data.get('password', '').strip()

        if not new_password:
            return Response({'password': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                account.user.set_password(new_password)
                account.user.save()
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        send_custom_email('Bonds | Senha Alterada com Sucesso', account.email, 'change_password_email.html', {'account': account})

        return Response({'detail': 'Account password updated successfully.'}, status=status.HTTP_200_OK)


class UpdateAccountProfileImage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image sent.'}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']

        if image.size > MAX_FILE_SIZE:
            return Response({'error': 'File size exceeds 5MB.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            img = Image.open(image)
            if img.format not in ['JPEG', 'PNG']:
                return Response({'error': 'Unsupported file format. Please upload JPEG or PNG.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'Invalid image file.'}, status=status.HTTP_400_BAD_REQUEST)

        img_low_res = img.copy()
        img_low_res.thumbnail((160, 160))

        if img_low_res.mode != 'RGB':
            img_low_res = img_low_res.convert('RGB')

        low_res_io = BytesIO()
        img_low_res.save(low_res_io, format='JPEG')
        low_res_io.seek(0)

        low_res_image = ContentFile(low_res_io.read(), name=f'low_res_{image.name.rsplit('.', 1)[0]}.jpeg')

        try:
            with transaction.atomic():
                account = request.user.account

                if account.profile_image:
                    old_image_path = account.profile_image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                    old_image_low_path = account.profile_image_low.path
                    if os.path.exists(old_image_low_path):
                        os.remove(old_image_low_path)

                account.profile_image = image
                account.profile_image_low = low_res_image
                account.save()
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        image_url = request.build_absolute_uri(account.profile_image.url)
        return Response({'message': 'Profile image updated successfully.', 'image_url': image_url}, status=status.HTTP_200_OK)


class AnonymizeAccountView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account = request.user.account
        
        try:
            with transaction.atomic():
                account.anonymize()
                Token.objects.filter(user=account.user).delete()
        except Exception as e:
            return Response({'detail': f'An error occurred while anonymizing the account: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Account anonymized successfully.'}, status=status.HTTP_200_OK)


class UpdateNeighborhoodView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account = request.user.account
        neighborhood_id = request.data.get('neighborhood_id', None)

        if not neighborhood_id:
            return Response({'neighborhood_id': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        except Neighborhood.DoesNotExist:
            return Response({'neighborhood_id': 'Invalid neighborhood ID.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():

                if account.last_neighborhood_change:
                    six_months_ago = now() - timedelta(days=6 * 30)
                    if account.last_neighborhood_change > six_months_ago:
                        remaining_time = (account.last_neighborhood_change + timedelta(days=6 * 30)) - now()
                        return Response({
                            'detail': 'You cannot change neighborhoods yet.',
                            'remaining_time': f'{remaining_time.days} days remaining.'
                        }, status=status.HTTP_400_BAD_REQUEST)

                current_user_profile = UserProfile.objects.get(account=account, active=True)
                current_user_profile.active = False
                current_user_profile.save()

                try:
                    new_user_profile = UserProfile.objects.get(account=account, neighborhood=neighborhood)
                    new_user_profile.active = True
                    new_user_profile.save()
                except UserProfile.DoesNotExist:
                    UserProfile.objects.create(account=account, neighborhood=neighborhood, active=True)

                account.last_neighborhood_change = now()
                account.save()

        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Neighborhood updated successfully.'}, status=status.HTTP_200_OK)
