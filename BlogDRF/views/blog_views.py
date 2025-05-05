from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from Blog.models import Blog, Like
from BlogDRF.permissions import IsNotAdminUser
from BlogDRF.serializers import BlogSerializer, CommentSerializer


class BlogList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = BlogSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            print(serializer.validated_data["category"])
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return None

    def get(self, request, pk):
        blog = self.get_object(pk)
        print()
        if blog is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)

        if blog.user != request.user:
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        if blog.user != request.user:
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogLike(APIView):
    permission_classes = [IsNotAdminUser]

    def post(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        if not blog:
            return Response(
                {"detail": "Blog not found."}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            like.delete()
            status = "unliked"
            code = status.HTTP_200_OK
        else:
            status = "liked"
            code = status.HTTP_201_CREATED

        like_count = blog.likes.count()
        return Response({"status": status, "like_count": like_count}, status=code)


class BlogComment(APIView):
    permission_classes = [IsNotAdminUser]

    def post(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        if not blog:
            return Response(
                {"detail": "Blog not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogApproved(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(
                {"detail": "Blog not found."}, status=status.HTTP_404_NOT_FOUND
            )

        blog.status = "approve"
        blog.save()

        return Response(
            {
                "message": "Blog status updated successfully.",
                "blog_id": str(blog.id),
                "status": blog.status,
            },
            status=status.HTTP_200_OK,
        )


class BlogRejected(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(
                {"detail": "Blog not found."}, status=status.HTTP_404_NOT_FOUND
            )

        blog.status = "reject"
        blog.save()

        return Response(
            {
                "message": "Blog status updated successfully.",
                "blog_id": str(blog.id),
                "status": blog.status,
            },
            status=status.HTTP_200_OK,
        )
