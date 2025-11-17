from rest_framework import serializers
from .models import Location, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class LocationSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)

    category = CategorySerializer(read_only=True)

    # Додано: Дозволяє призначати категорію за її ID (тільки для запису)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',  # Вказує, що це поле оновлює 'category'
        write_only=True,
        allow_null=True,
        required=False
    )


    class Meta:
        model = Location
        fields = [
            'id', 'name', 'address', 'coordinates',
            'author',
            'category', 'category_id',
            'avg_rating'
        ]
        read_only_fields = [
            'id',
            'author',
            'avg_rating',
            'category'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'location',
            'author', 'author_username',
            'rating', 'comment',
            'created_at',
            'likes_count', 'dislikes_count',
        ]
        read_only_fields = ['id', 'author', 'created_at']

#    def validate(self, data):
#        request = self.context.get('request')
#        if request and hasattr(request, 'user'):
#            author = request.user
#            location = data['location']
#
#            # Перевіряємо, чи існує відгук (окрім того, що ми редагуємо)
#            queryset = Review.objects.filter(location=location, author=author)
#            if self.instance:  # Якщо це UPDATE (PUT/PATCH)
#                queryset = queryset.exclude(pk=self.instance.pk)
#
#            if queryset.exists():
#                raise serializers.ValidationError(
#                    "Ви вже залишили відгук для цієї локації."
#                )
#        return data