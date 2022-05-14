from rest_framework import serializers

from ads.models import Category, Ad


class NotTrueValidator:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError("new ad can not be published")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='first_name',
        read_only=True,
    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author_id", "author", "price", "description", "is_published", "category_id", "image"]


class AdCreateSerializer(serializers.ModelSerializer):
    author = serializers.BooleanField(validators=[NotTrueValidator()])

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
