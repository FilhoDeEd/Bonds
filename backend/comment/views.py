from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from account.views import add_errors
from rest_framework.response import Response
from rest_framework import status

from comment.models import Comment
from comment.serializers import CommentSerializer
from user_profile.models import UserProfile




class CommentRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        errors = {}

        comment_serializer = CommentSerializer(data=data)

        if not comment_serializer.is_valid():
             add_errors(errors=errors, serializer_errors=comment_serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Obtém o perfil do usuário logado
                account = request.user.account
                user_profile = UserProfile.objects.get(account=account, active=True)

                # Cria o comentário
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