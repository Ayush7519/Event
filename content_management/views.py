import os

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from account.renders import UserRenderer
from ems.pagination import MyPageNumberPagination

from .models import Blog, Comment, Content_Management, Heading
from .serializer import (
    BlogSerializer,
    CommentCustomSerializer,
    CommentSerializer,
    Content_ManagementListSerializer,
    Content_ManagementSerializer,
    HeadingSerializer,
    ImageUploaderSerializer,
)


# creating the view for the image uploader.
class ImageUploadApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        serializer = ImageUploaderSerializer(
            data=request.data,
            context={"user": request.user},
        )
        if serializer.is_valid(raise_exception=True):
            uploaded_file = serializer.validated_data["file"]
            print(uploaded_file)
            # creating the path to save the image.
            file_path = os.path.join(
                settings.MEDIA_ROOT, "CMS_Photos", uploaded_file.name
            )
            # writing in the file.
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            url = request.build_absolute_uri(
                settings.MEDIA_URL + "CMS_Photos/" + uploaded_file.name
            )
            print(url)
            return Response(
                {"url": url},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


# heading
# heading created.
class HeadingCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    queryset = Heading.objects.all()
    serializer_class = HeadingSerializer


# heading list.
class HeadingListApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    queryset = Heading.objects.all()
    serializer_class = HeadingSerializer


# content_management
# content_management creating.
class Content_ManagementCreateApiView(APIView):
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = Content_ManagementSerializer(data=request.data)
        if serializer.is_valid():
            # to update the model fields data after the serializer this methods is used.
            serializer.validated_data["updated_by"] = request.user.name
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# content-management list with search.
class Content_ManagementSearchApiView(generics.ListAPIView):
    queryset = Content_Management.objects.all()
    serializer_class = Content_ManagementSerializer
    filter_backends = [SearchFilter]
    search_fields = ["heading"]
    pagination_class = MyPageNumberPagination
    permission_classes = [permissions.IsAdminUser]


# content-management draft list only.
class Content_ManagementStatusListApiView(APIView, PageNumberPagination):
    permission_classes = [permissions.IsAdminUser]
    page_size = 10

    def get(self, request, status, format=None, *args, **kwargs):
        if status == "Draft" or status == "Publish":
            queryset = Content_Management.objects.filter(status=status)
            results = self.paginate_queryset(queryset, request, view=self)
            serializer = Content_ManagementSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        elif status == "All":
            queryset = Content_Management.objects.all()
            results = self.paginate_queryset(queryset, request, view=self)
            serializer = Content_ManagementSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        else:
            return Response({"msg": "Check your status.That doesn't match our status"})


# content-management update.
class Content_managementUpdateApiView(generics.UpdateAPIView):
    queryset = Content_Management.objects.all()
    serializer_class = Content_ManagementSerializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [UserRenderer]


# content-management delete.
class Content_ManagementDeleteApiView(generics.DestroyAPIView):
    queryset = Content_Management.objects.all()
    serializer_class = Content_ManagementSerializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [UserRenderer]


# this for making the dynamic webpage.
# content-management for the front end user.
class Contetn_Manageent_ButtonListApiView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, pk, *args, **kwargs):
        print(pk)
        try:
            heading_info = Heading.objects.get(id=pk)
            print(heading_info)
        except Heading.DoesNotExist:
            return Response(
                {"msg": "Searched Heading is not available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        cms_info = Content_Management.objects.filter(heading=heading_info)
        print(cms_info)
        serializer = Content_ManagementListSerializer(cms_info, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# View For The Blog.
# this is for the tinymc for the blog part.
class BlogImageUploadApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        serializer = ImageUploaderSerializer(
            data=request.data,
            context={"user": request.user},
        )
        if serializer.is_valid(raise_exception=True):
            uploaded_file = serializer.validated_data["file"]
            print(uploaded_file)
            # creating the path to save the image.
            file_path = os.path.join(
                settings.MEDIA_ROOT, "Blog_Photos", uploaded_file.name
            )
            # writing in the file.
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            url = request.build_absolute_uri(
                settings.MEDIA_URL + "Blog_Photos/" + uploaded_file.name
            )
            print(url)
            return Response(
                {"url": url},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


# blog created view.
class BlogCreateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user.username
            data = "Null"
            print(user)
            serializer.validated_data["created_by"] = user
            serializer.validated_data["updated_by"] = data
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# blog list. tis give the full list of the blog.
class BlogListApiView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by("-date_created")
    serializer_class = BlogSerializer


# blog search.
class BlogSearchApiView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter]
    search_fields = ["^created_by"]


# blog update
class BlogUpdateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk, *args, **kwargs):
        try:
            blog_data = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response(
                {"msg": f"Blog with the id {pk} is not available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BlogSerializer(blog_data, data=request.data)
        if serializer.is_valid():
            user = request.user.username
            print(user)
            serializer.validated_data["updated_by"] = user
            serializer.save()
            return Response(
                serializer.data,
                headers={"msg": "Data is updated"},
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# blog delete.
class BlogDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


# blog detail view for the user.
class BlogDetailApiView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    renderer_classes = [UserRenderer]


# for the comment model.
# comment create.
class CommentCreateApiView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, id, *args, **kwargs):
        blog = Blog.objects.get(pk=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["blog"] = blog
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# comment list.
class CommentListApiView(generics.ListAPIView):
    serializer_class = CommentCustomSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        id = self.kwargs["id"]
        return Comment.objects.filter(blog=id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(
                queryset,
                many=True,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                "No comments found for this blog",
                status=status.HTTP_404_NOT_FOUND,
            )
