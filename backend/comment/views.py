import os
from PIL import Image

from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from account.views import add_errors
from rest_framework.response import Response
from rest_framework import status
from forum.models import Forum

from comment.models import Comment, Like, Report, Pool, Option, Vote
from comment.serializers import CommentSerializer, ReportSerializer, PoolSerializer, OptionSerializer, PoolEditSerializer
from user_profile.models import UserProfile


MAX_FILE_SIZE = 5 * 1024 * 1024


class CommentRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        errors = {}

        # Obter o slug do fórum e buscar o objeto correspondente
        forum_slug = data.get('forum_slug')
        forum = get_object_or_404(Forum, slug=forum_slug)
        data['forum'] = forum.id  # Substituir pelo ID do fórum

        comment_serializer = CommentSerializer(data=data)

        if not comment_serializer.is_valid():
            add_errors(errors=errors, serializer_errors=comment_serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                account = request.user.account
                user_profile = UserProfile.objects.get(account=account, active=True)

                # Criar o comentário
                comment = comment_serializer.save(user_profile=user_profile)

        except Exception as e:
            return Response({'detail': f'An unexpected error occurred. {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Comment created successfully.', 'id': comment.id}, status=status.HTTP_201_CREATED)
    

class CommentEditView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        # Obtém o comentário pelo ID
        comment = get_object_or_404(Comment, id=comment_id)

        account = request.user.account
        try:
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Invalid or inactive user."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o usuário logado é o dono do comentário
        if comment.user_profile != user_profile:
            return Response({"detail": "You do not have permission to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        # Atualiza os dados do comentário
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Comment updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommentImageUpdateView(APIView):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

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

        if img.mode != 'RGB':
            img = img.convert('RGB')

        try:
            if comment.image:
                old_image_path = comment.image.path
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            comment.image = image
            comment.save()
        except Exception as e:
            return Response({'error': f'An error occurred while saving the image: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        image_url = request.build_absolute_uri(comment.image.url)
        return Response({'message': 'Comment image updated successfully.', 'image_url': image_url}, status=status.HTTP_200_OK)


class CommentDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        # Obtém o comentário pelo ID
        comment = get_object_or_404(Comment, id=comment_id)

        account = request.user.account
        try:
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Active user profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o usuário logado é o dono do comentário
        if comment.user_profile != user_profile:
            return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        # Deleta o comentário
        comment.delete()

        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_200_OK)
    
class CommentListView(ListAPIView):
    """
    Lista os comentários de um fórum específico, filtrando pelo slug do fórum.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Obtém o slug do fórum da URL
        forum_slug = self.kwargs.get('slug')
        # Busca o fórum correspondente ou retorna 404
        forum = get_object_or_404(Forum, slug=forum_slug)
        # Retorna os comentários relacionados ao fórum encontrado
        return Comment.objects.filter(forum=forum, type= Comment.TypeChoices.COMMENT)
    
class ReportListView(ListAPIView):
    """
    Lista os comentários de um fórum específico, filtrando pelo slug do fórum.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer

    def get_queryset(self):
        # Obtém o slug do fórum da URL
        forum_slug = self.kwargs.get('slug')
        # Busca o fórum correspondente ou retorna 404
        forum = get_object_or_404(Forum, slug=forum_slug)
        # Retorna os comentários relacionados ao fórum encontrado
        return Report.objects.filter(forum=forum)
    

class LikeView(APIView):
    """
    Adiciona um like a um comentário.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user_profile = self.get_user_profile(request)

        # Adiciona ou atualiza o like
        like_instance, created = Like.objects.update_or_create(
            user_profile=user_profile,
            comment=comment,
            defaults={'is_like': True}  # Like
        )

        return Response({
            "detail": "Like added successfully.",
            "trust_rate": comment.trust_rate()
        }, status=status.HTTP_200_OK)

    def get_user_profile(self, request):
        account = request.user.account
        return get_object_or_404(UserProfile, account=account, active=True)


class DislikeView(APIView):
    """
    Adiciona um dislike a um comentário.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user_profile = self.get_user_profile(request)

        # Adiciona ou atualiza o dislike
        like_instance, created = Like.objects.update_or_create(
            user_profile=user_profile,
            comment=comment,
            defaults={'is_like': False}  # Dislike
        )

        return Response({
            "detail": "Dislike added successfully.",
            "trust_rate": comment.trust_rate()
        }, status=status.HTTP_200_OK)

    def get_user_profile(self, request):
        account = request.user.account
        return get_object_or_404(UserProfile, account=account, active=True)


class LikeDeleteView(APIView):
    """
    Remove um like ou dislike de um comentário.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user_profile = self.get_user_profile(request)

        # Remove o like/dislike
        deleted, _ = Like.objects.filter(user_profile=user_profile, comment=comment).delete()

        if deleted:
            return Response({
                "detail": "Interaction removed successfully.",
                "trust_rate": comment.trust_rate()
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "No interaction to remove."
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_user_profile(self, request):
        account = request.user.account
        return get_object_or_404(UserProfile, account=account, active=True)
    
class ReportRegisterView(APIView):
    """
    Registra um novo report.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        errors = {}

         # Obter o slug do fórum e buscar o objeto correspondente
        forum_slug = data.get('forum_slug')
        forum = get_object_or_404(Forum, slug=forum_slug)
        data['forum'] = forum.id  # Substituir pelo ID do fórum


        serializer = ReportSerializer(data=data)

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                account = request.user.account
                user_profile = get_object_or_404(UserProfile, account=account, active=True)
                report = serializer.save(user_profile=user_profile, type = 'R')
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred. {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Report created successfully.', 'id': report.id}, status=status.HTTP_201_CREATED)

class ReportEditView(APIView):
    """
    Edita um report existente.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        """
        Atualiza os dados de um report pelo ID.
        """
        try:
            # Obtém o report pelo ID
            report = get_object_or_404(Report, pk=report_id)

            account = request.user.account
            try:
                user_profile = UserProfile.objects.get(account=account, active=True)
            except UserProfile.DoesNotExist:
                return Response({"detail": "Invalid or inactive user."}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica se o usuário é o dono do report
            if report.user_profile != user_profile:
                return Response({"detail": "You do not have permission to edit this report."}, status=status.HTTP_403_FORBIDDEN)


            # Valida e atualiza o report
            serializer = ReportSerializer(report, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": "Report updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"detail": f"Ocorreu um erro inesperado. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ReportDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        # Obtém o comentário pelo ID
        report = get_object_or_404(Report, id=report_id)

        account = request.user.account
        try:
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Active user profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o usuário logado é o dono do comentário
        if report.user_profile != user_profile:
            return Response({"detail": "You do not have permission to delete this report."}, status=status.HTTP_403_FORBIDDEN)

        # Deleta o comentário
        report.delete()

        return Response({"detail": "Report deleted successfully."}, status=status.HTTP_200_OK)
    

class PoolRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        errors = {}

        # Obter o slug do fórum e buscar o objeto correspondente
        forum_slug = data.get('forum_slug')
        forum = get_object_or_404(Forum, slug=forum_slug)
        data['forum'] = forum.id  # Substituir pelo ID do fórum

        pool_serializer = PoolSerializer(data=data)

        if not pool_serializer.is_valid():
            add_errors(errors=errors, serializer_errors=pool_serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                account = request.user.account
                user_profile = UserProfile.objects.get(account=account, active=True)

                # Criar a Pool
                pool = pool_serializer.save(user_profile=user_profile)

                # Criar as opções associadas
                options_data = data.get('options', [])
                for option_data in options_data:
                    Option.objects.create(pool=pool, **option_data)

        except Exception as e:
            return Response({'detail': f'An unexpected error occurred. {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Pool created successfully.', 'id': pool.id}, status=status.HTTP_201_CREATED)



class PoolEditView(APIView):
    """
    View para editar os campos title, content e deadline de uma Pool usando POST.
    """
    def post(self, request, pool_id):
        # Obtém o Pool pelo ID (pk) ou retorna 404 se não encontrado
        pool = get_object_or_404(Pool, id=pool_id)

        # Usa o serializer para validar e atualizar os dados
        serializer = PoolEditSerializer(pool, data=request.data, partial=True)

        if serializer.is_valid():
            # Salva as alterações no objeto Pool
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PoolDeleteView(APIView):
    """
    View para deletar uma Pool com base no ID (pk), utilizando o método POST.
    """
    def post(self, request, pool_id):
        # Obtém o Pool pelo ID (pool_id) ou retorna 404 se não encontrado
        pool = get_object_or_404(Pool, id=pool_id)

        # Exclui o Pool
        pool.delete()

        # Retorna uma resposta de sucesso
        return Response({"message": "Pool deletada com sucesso."}, status=status.HTTP_204_NO_CONTENT)


class PoolListView(ListAPIView):
    """
    Lista as pools de um fórum específico, filtrando pelo slug do fórum e incluindo as opções associadas.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PoolSerializer

    def get_queryset(self):
        # Obtém o slug do fórum da URL
        forum_slug = self.kwargs.get('slug')
        # Busca o fórum correspondente ou retorna 404
        forum = get_object_or_404(Forum, slug=forum_slug)
        # Retorna as pools relacionadas ao fórum encontrado e prefetch as opções associadas
        return Pool.objects.filter(forum=forum).prefetch_related('options')
    
class VoteOptionView(APIView):
    """
    View para registrar um voto em uma opção, vinculado ao usuário.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, option_id):
        # Obter o perfil do usuário logado
        try:
            account = request.user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Perfil de usuário ativo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Obter a opção pelo ID ou retornar 404
        option = get_object_or_404(Option, id=option_id)

        # Verificar se o usuário já votou nesta opção
        if Vote.objects.filter(user_profile=user_profile, option=option).exists():
            return Response({'detail': 'Você já votou nesta opção.'}, status=status.HTTP_400_BAD_REQUEST)

        # Criar o registro de voto
        Vote.objects.create(user_profile=user_profile, option=option)

        # Incrementar o número de votos na opção
        option.votes += 1
        option.save()

        return Response({
            'id': option.id,
            'option_text': option.option_text,
            'votes': option.votes,
        }, status=status.HTTP_201_CREATED)


class UnvoteOptionView(APIView):
    """
    View para remover um voto de uma opção, vinculado ao usuário.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, option_id):
        # Obter o perfil do usuário logado
        try:
            account = request.user.account
            user_profile = UserProfile.objects.get(account=account, active=True)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Perfil de usuário ativo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Obter a opção pelo ID ou retornar 404
        option = get_object_or_404(Option, id=option_id)

        # Verificar se o usuário votou nesta opção
        vote = Vote.objects.filter(user_profile=user_profile, option=option).first()
        if not vote:
            return Response({'detail': 'Você ainda não votou nesta opção.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remover o registro de voto
        vote.delete()

        # Decrementar o número de votos na opção, se maior que 0
        if option.votes > 0:
            option.votes -= 1
            option.save()

        return Response({
            'id': option.id,
            'option_text': option.option_text,
            'votes': option.votes,
        }, status=status.HTTP_200_OK)