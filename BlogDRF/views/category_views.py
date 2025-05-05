from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from BlogDRF.permissions import CategoryPermission

from Blog.models import Category
from BlogDRF.serializers import CategorySerializer


class CategoryView(APIView):
    permission_classes = [CategoryPermission]

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [permissions.AllowAny]
    #     else:
    #         return [permissions.IsAdminUser]

    def get(self, request):
        blogs = Category.objects.all()
        serializer = CategorySerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        print(request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDelete(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"detail": "Category Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
