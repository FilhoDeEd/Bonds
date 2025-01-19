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

from comment.models import Comment, Like, Report
from comment.serializers import CommentSerializer, ReportSerializer
from user_profile.models import UserProfile





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
   