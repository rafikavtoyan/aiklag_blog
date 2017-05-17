from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)

from comments.api.serializers import CommentSerializer
from comments.models import Comment

from ..models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish'
        ]


class PostDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'html',
            'image',
            'user',
            'publish',
            'comments'
        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            return obj.image.url
        except Exception as e:
            return None

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug'
    )
    user = SerializerMethodField()

    # delete_url = HyperlinkedIdentityField(
    #     view_name='posts-api:delete',
    #     lookup_field='slug'
    # )

    class Meta:
        model = Post
        fields = [
            'url',
            # 'delete_url',
            'user',
            'title',
            'content',
            'publish'
        ]

    def get_user(self, obj):
        return str(obj.user.username)

