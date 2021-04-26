from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from watchlist_app.models import Movie


class MovieSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    status_value = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'active', 'status_value')
        # exclude = ['description']

    def create(self, validated_data):
        if validated_data.get('name') == validated_data.get('description'):
            raise ValidationError(
                {'message': "Cannot be same both desc and name"})
        return super().create(validated_data)

    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError({
                "message": "Cannot be less than 3 chars"
            })
        return value

    def get_status_value(self, object):
        if object.active:
            return "Active Film"
        else:
            return "Expired Film"

# class MovieSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         # movie = Movie.objects.filter(pk=instance.id)
#         # return movie(**validated_data)
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
