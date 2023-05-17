from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('title', 'author', 'text', 'score', 'pub_date')
        read_only = ('pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('title', 'author', 'text', 'pub_date')
        read_only = ('pub_date')
