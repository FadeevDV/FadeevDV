from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ['title']
        model = Review

    def validate(self, data):
        """
        Check that the score is between 1 and 10.
        """
        if 0 < data['score'] <= 10:
            return data
        raise serializers.ValidationError({'score': 'out of possible range'})


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ['review']
        model = Comment
