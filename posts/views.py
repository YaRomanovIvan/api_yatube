from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        if not request.auth:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def partial_update(self, request, post_id, pk):
        comment = get_object_or_404(Comment, post=post_id, pk=pk)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, post_id):
        queryset = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, post_id, pk):
        comment = get_object_or_404(Comment, post=post_id, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, post_id, pk):
        comment = get_object_or_404(Comment, post=post_id, pk=pk)
        if comment.author != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, post_id, pk):
        comment = get_object_or_404(Comment, post=post_id, pk=pk)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
