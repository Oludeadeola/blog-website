from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from .models import Post, Comment

PUBLISHER_INDEX = Index(name="Post")
PUBLISHER_INDEX.settings(number_of_shards=1, number_of_replicas=1)


@PUBLISHER_INDEX.doc_type
class PostsDocument(Document):
    id = fields.IntegerField(attr="id")
    title = fields.TextField(fields={"raw": {"type": "keyword"}})
    body = fields.TextField(fields={"raw": {"type": "keyword"}})

    class Django(object):
        model = Post


@registry.register_document
class CommentDocument(Document):

    author_name = fields.TextField(attr="get_author_name")

    class Index:
        name = "Comment"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
        }

    class Django(object):
        model = Comment
        fields = ["id", "body"]
        extra_kwargs = {
            "id": {"type": "integer"},
            "body": {"type": "keyword"},
        }

    def get_author_name(self, instance):
        return instance.author.username
