from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from forum.serializers import ForumSerializer, ForumListSerializer, ForumEditSerializer, EventSerializer, EventEditSerializer, ReviewSerializer, ReviewEditSerializer
from account.views import add_errors
from forum.models import Forum , Subscriber , Event , Review
from django.utils.text import slugify


from rest_framework import status
from rest_framework.response import Response

from user_profile.models import UserProfile


class ForumRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        forum_serializer = ForumSerializer(data=data)

        errors = {}

        if not forum_serializer.is_valid():
            add_errors(errors=errors, serializer_errors=forum_serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                account = request.user.account
                user_profile = UserProfile.objects.get(account=account, active=True)
                forum = forum_serializer.save(owner=user_profile, neighborhood=user_profile.neighborhood)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred. {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Success.', 'slug': forum.slug}, status=status.HTTP_201_CREATED)


class ForumListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ForumListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['subscribers_count', 'popularity', 'creation_date']
    ordering = ['-creation_date']

    def get_queryset(self):
        account = self.request.user.account
        
        try:
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Forum.objects.none()
        
        neighborhood = user_profile.neighborhood
        return Forum.objects.filter(neighborhood=neighborhood)


class ForumDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        forum = get_object_or_404(Forum, slug=slug)
        serializer = ForumSerializer(forum)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForumEditView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        # Obtém o fórum pelo slug
        forum = get_object_or_404(Forum, slug=slug)

        account = self.request.user.account

        try:
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Invalid or inactive user."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o usuário logado é o dono do fórum
        if forum.owner != user_profile:
            return Response({"detail": "You do not have permission to edit this forum."}, status=status.HTTP_403_FORBIDDEN)

        # Atualiza os dados e ajusta o slug com base no título
        forum_serializer = ForumEditSerializer(forum, data=request.data)
        if forum_serializer.is_valid():
            forum = forum_serializer.save()  # Salva os dados validados
            # Atualiza o slug com base no novo título
            forum.slug = slugify(forum.title)
            forum.save()
            return Response({"success": "success", "slug": forum.slug}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": forum_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForumDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        # Obtém o fórum pelo slug
        forum = get_object_or_404(Forum, slug=slug)

        # Obtém a conta do usuário logado
        account = self.request.user.account
        
        try:
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Perfil de usuário ativo não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o usuário logado é o dono do fórum
        if forum.owner != user_profile:
            return Response({"detail": "Você não tem permissão para excluir este fórum."}, status=status.HTTP_403_FORBIDDEN)

        # Deleta o fórum
        forum.delete()

        return Response({"detail": "Fórum excluído com sucesso."}, status=status.HTTP_200_OK)

class EventRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        event_serializer = EventSerializer(data=data)
        errors = {}

        if not event_serializer.is_valid():
            add_errors(errors=errors, serializer_errors=event_serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                account = request.user.account
                user_profile = UserProfile.objects.get(account=account, active=True)
                event = event_serializer.save(owner=user_profile, neighborhood=user_profile.neighborhood, type = 'E')
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred. {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Event created successfully.', 'slug': event.slug}, status=status.HTTP_201_CREATED)




class EventEditView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        account = request.user.account

        try:
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Invalid or inactive user."}, status=status.HTTP_400_BAD_REQUEST)

        if event.owner != user_profile:
            return Response({"detail": "You do not have permission to edit this event."}, status=status.HTTP_403_FORBIDDEN)

        event_serializer = EventEditSerializer(event, data=request.data)
        if event_serializer.is_valid():
            event = event_serializer.save()
            event.slug = slugify(event.title)
            event.save()
            return Response({"success": "Event updated successfully.", "slug": event.slug}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": event_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class SubscribeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:

            forum = Forum.objects.get(slug=slug)
        except Forum.DoesNotExist:
            return Response({'detail': 'Forum not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:

            account = request.user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Active user profile not found.'}, status=status.HTTP_404_NOT_FOUND)


        if Subscriber.objects.filter(user_profile=user_profile, forum=forum).exists():
            return Response({'detail': 'User already subscribed to this forum.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():

                Subscriber.objects.create(user_profile=user_profile, forum=forum)

    
                forum.subscribers_count += 1
                forum.save()

            return Response({'detail': 'Successfully subscribed to the forum.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': f'An error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnsubscribeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:
            # Obtém o fórum pelo slug
            forum = Forum.objects.get(slug=slug)
        except Forum.DoesNotExist:
            return Response({'detail': 'Forum not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Obtém o perfil do usuário logado
            account = request.user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Active user profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se o usuário já está inscrito no fórum
        try:
            subscription = Subscriber.objects.get(user_profile=user_profile, forum=forum)
        except Subscriber.DoesNotExist:
            return Response({'detail': 'User is not subscribed to this forum.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Remove a inscrição
                subscription.delete()

                # Atualiza o contador de inscritos no fórum
                forum.subscribers_count -= 1
                forum.save()

            return Response({'detail': 'Successfully unsubscribed from the forum.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': f'An error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        errors = {}

        forum_slug = data.get('forum_slug')
        forum = get_object_or_404(Forum, slug=forum_slug)
        data['forum'] = forum.id 
        
        try:
            account = request.user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Perfil de usuário não encontrado ou inativo."}, status=status.HTTP_400_BAD_REQUEST)

        event_id = data.get('event')
        event = get_object_or_404(Event, id=event_id)

        # Verifica se o usuário já fez uma review para este evento
        if Review.objects.filter(event=event, user=user_profile).exists():
            return Response({"detail": "Você já avaliou este evento."}, status=status.HTTP_400_BAD_REQUEST)

        review_data = {
            "event": event.id,
            "user": user_profile.id,
            "five_star": data.get("five_star")
        }

        review_serializer = ReviewSerializer(data=review_data)
        if not review_serializer.is_valid():
            add_errors(errors=errors, serializer_errors=review_serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        review = review_serializer.save()
        event.calculate_five_star_mean()  # Atualiza a média de avaliações do evento

        return Response({"detail": "Review registrada com sucesso."}, status=status.HTTP_201_CREATED)
