from pytest_factoryboy import register

from tests.factories import UserFactory, CategoryFactory, AdFactory

pytest_plugins = "test.fixtures"

register(UserFactory)
register(CategoryFactory)
register(AdFactory)
