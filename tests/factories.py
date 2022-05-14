import factory

from ads.models import Category, Ad
from users.models import User


class NameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker("name")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    slug = factory.Faker("color")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("color")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.SubFactory(NameFactory)
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    price = 10
