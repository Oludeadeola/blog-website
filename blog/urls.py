from django.urls import path
from blog.views import (
    BloggerPostsListView,
    BloggerPostRetrieveView,
    PostCreateView,
    PostsListView,
    BloggerPostDestroyView,
    PostRetrieveView,
    BloggerPostUpdateView,
    AddCommentView,
    AddLikeView,
    PostDocumentView,
)

urlpatterns = [
    path("post/create-new", PostCreateView.as_view()),
    path("search/", PostDocumentView.as_view({"get": "list"})),
    path("post/<uuid:pid>/add-comment", AddCommentView.as_view()),
    path("post/<uuid:pid>/add-like", AddLikeView.as_view()),
    path("blogger/<uuid:bid>/posts/", BloggerPostsListView.as_view()),
    path("blogger/<uuid:bid>/post/<uuid:pid>/", BloggerPostRetrieveView.as_view()),
    path("post/<uuid:pid>/", PostRetrieveView.as_view()),
    path(
        "post/<uuid:pid>/delete-post",
        BloggerPostDestroyView.as_view(lookup_field="uuid"),
    ),
    path("post/<uuid:pid>/update-post", BloggerPostUpdateView.as_view()),
    path("posts/all/", PostsListView.as_view()),
]
