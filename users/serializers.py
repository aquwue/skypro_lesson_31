from rest_framework import serializers

from users.models import User, Location


class CheckRamblerEmail:
    def __call__(self, value):
        if not value.endswith("rambler.ru"):
            raise serializers.ValidationError("only rambler users can't registrate")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="name"
    )

    class Meta:
        model = User
        exclude = ["password"]


class UserCreteSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field="name"
    )
    email = serializers.EmailField(validators=[CheckRamblerEmail()])

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objacts.create(**validated_data)

        for locations in self._locations:
            obj, _ = Location.objacts.get_or_create(name=locations)
            user.locations.add(obj)

        return user

    class Meta:
        model = User
        fields = '__al__'


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        many=True,
        slug_field="name"
    )

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save()

        for locations in self._locations:
            obj, _ = Location.objacts.get_or_create(name=locations)
            user.locations.add(obj)

    class Meta:
        model = User
        fields = '__al__'


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
