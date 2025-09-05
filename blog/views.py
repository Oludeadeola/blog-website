from django_elasticsearch_dsl_drf.filter_backends import (
    SearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)

from auths.models import Blogger
from auths.permissions import IsAuthenticatedUser
from blog.document import PostsDocument
from blog.models import Media, Post, Comment, Like
from blog.querysets import ALL_POSTS_QUERYSET
from blog.serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    LikeSerializer,
    PostDocumentSerializer,
)
from blog.filters import PostFilter
from commons.utils import get_object_or_404


# region Base Classes
class PostAPIView(GenericAPIView):
    queryset = ALL_POSTS_QUERYSET
    serializer_class = PostSerializer
    filter_class = PostFilter
    permission_classes = [IsAuthenticatedUser]
    search_fields = [
        "title",
        "blogger__username",
        "blogger__email",
        "id",
        "uuid",
        "created_at",
    ]
    ordering_fields = ["title", "created_at"]
    ordering = ["-created_at"]


# endregion
# region Post - Public(Not User Endpoint)


class PostCreateView(CreateModelMixin, PostAPIView):
    serializer_class = PostCreateSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            blogger: Blogger = get_object_or_404(
                Blogger, email=request.data.get("blogger_email")
            )
            data: dict = serializer.validated_data
            data["blogger"] = blogger
            data["status"] = Post.Status.PUBLISHED
            post: Post = self.perform_create(data=data)
            headers = self.get_success_headers(serializer.data)
            response_serializer = PostSerializer(post)
            return Response(
                data={
                    "message": "Post created successfully",
                    **response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as exception:
            return Response(
                data={"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, data: dict) -> Post:
        unwanted_data_keys = ["blogger_email", "media_urls"]
        post: Post = Post.objects.create(
            **{
                key: value
                for key, value in data.items()
                if key not in unwanted_data_keys
            }
        )
        media_urls = data.get("media_urls")
        medias = [Media(cloud_url=url, post=post) for url in media_urls]
        Media.objects.bulk_create(medias)
        return post


class PostsListView(ListModelMixin, PostAPIView):

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostRetrieveView(RetrieveModelMixin, PostAPIView):

    def get(self, request, *args, **kwargs):
        post: Post = self.get_queryset().filter(uuid=kwargs.get("bid")).get()
        serializer: PostSerializer = self.get_serializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AddCommentView(CreateModelMixin, PostAPIView):
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        serializer: CommentSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post: Post = ALL_POSTS_QUERYSET.get(uuid=kwargs.get("pid"))
        author: Blogger = get_object_or_404(
            Blogger, username=serializer.validated_data.get("author").get("username")
        )
        comment: Comment = Comment.objects.create(
            body=serializer.validated_data.get("body"), post=post, author=author
        )
        response_serializer = self.get_serializer(comment)
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AddLikeView(CreateModelMixin, PostAPIView):
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        serializer: LikeSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post: Post = ALL_POSTS_QUERYSET.get(uuid=kwargs.get("pid"))
        post.number_of_likes = post.number_of_likes + 1
        post.save()
        creator: Blogger = get_object_or_404(
            Blogger, username=serializer.validated_data.get("creator").get("username")
        )
        like: Like = Like.objects.create(creator=creator, post=post)
        response_serializer = self.get_serializer(like)
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# endregion
# region - Post - Private(User Specific Endpoints)

"""
TODO: Endpoints To Add
1. Delete Post
2. Create Draft Post
3. Update Post
4. Get Blogger Specific Draft Post
"""


class BloggerPostsListView(ListModelMixin, PostAPIView):

    def get(self, request: Request, *args, **kwargs):
        blogger: Blogger = get_object_or_404(Blogger, uuid=kwargs.get("bid"))
        posts = self.get_queryset().filter(blogger=blogger)
        response_data = [self.get_serializer(post).data for post in posts]
        return Response(data=response_data, status=status.HTTP_200_OK)


class BloggerPostRetrieveView(RetrieveModelMixin, PostAPIView):

    def get(self, request, *args, **kwargs):
        blogger: Blogger = get_object_or_404(Blogger, uuid=kwargs.get("bid"))
        post: Post = (
            self.get_queryset().filter(blogger=blogger).get(uuid=kwargs.get("pid"))
        )
        serializer: PostSerializer = self.get_serializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BloggerPostDestroyView(DestroyModelMixin, PostAPIView):

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        pid = self.kwargs.get("pid")
        return get_object_or_404(Post, uuid=pid)


class BloggerPostUpdateView(UpdateModelMixin, PostAPIView):

    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class PostDocumentView(DocumentViewSet):
    document = PostsDocument
    serializer_class = PostDocumentSerializer
    filter_backends = [
        SearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
    search_fields = [
        "title",
        "blogger__username",
        "blogger__email",
        "uuid",
        "created_at",
    ]
    filter_fields = {
        "title": "title",
        "blogger__username": "blogger__username",
        "blogger__email": "blogger__email",
        "uuid": "uuid",
        "created_at": "created_at",
    }
    ordering_fields = ["title", "created_at"]
    multi_match_search_fields = ["title", "blogger__username", "blogger__email", "body"]
