from django.db.models import Q

from blog.models import Post, Blogger

ALL_POSTS_QUERYSET = Post.objects.filter(~Q(status=Post.Status.REMOVED))
PUBLISHED_POSTS_QUERYSET = Post.objects.filter(status=Post.Status.PUBLISHED)
ALL_BLOGGERS_QUERYSET = Blogger.objects.all()
